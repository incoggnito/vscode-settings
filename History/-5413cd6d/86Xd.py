import inspect
import signal

from measurementgui.ui_files.CMS_GUI import Ui_MainWindow
from measurementgui.utils.mqtt.mqtt_standard import init_mqtt

# from ui_files.CMS_GUI import Ui_MainWindow
from atoolbox import FileHandler
from vallendb.utils import read_acq_settings
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QDialog,
    QAction,
    QFileDialog,
    QHBoxLayout,
    QPushButton,
)
from PySide2 import QtCore
import sys
from pathlib import Path, PurePath
import pandas as pd
import numpy as np
import os
from typing import Optional, Union, Dict
import vallenae as vae
from fyrsonic.measurement import measurement_interface
from fyrsonic.measurement import trfdb_writer
import logging
from datetime import datetime
import sqlite3
import sys
import sqlalchemy as sa
import paho.mqtt.client as paho
from measurementgui.utils.mqtt.mqtt_standard import on_connect, on_connect_fail, on_disconnect

# [x] TODO get the logo and the Icon working again (currently the paths in the generates LaserDetectionGUI.py has to be adapted, only data/ressources/...)
# [x] TODO visualize active state with colored label
# [ ] TODO add a check which devices (conditionWave, TiePies) are connected -> user choice which one to use
# [ ] TODO config files for every device seperatly
# [x] TODO rolling mean of the plots

formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# LOGGER_IMPORTED_MODULES = logging.getLogger("asammdf")  # [ ] TODO not working
# LOGGER_IMPORTED_MODULES.setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)
today = datetime.today()
today_str = today.strftime("%Y_%m_%d")
LOGFILE = Path(r"data\logs", today_str + ".log").absolute()
ALARMLOGFILE = Path(r"data\alarm", today_str + ".db").absolute()
handler = logging.FileHandler(LOGFILE, mode="a+")
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(formatter)
# consoleHandler.setLevel(logging.DEBUG)
# LOGGER.addHandler(consoleHandler)
LOGGER.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.INFO)

# [ ] TODO get the lowpass filter working

# [ ] TODO better to use the filehandler here?
PYTHON_VENV = str(Path(r"venv\Scripts\python.exe").absolute())
CONFIGFILE_PATH = PurePath(r"data/settings/measurement_settings.json")
ALARMSETTINGSFILE_PATH = PurePath(r"data/settings/alarm_settings.yml")
DISPLAY_INTERVAL = 100  # ms
# arbitrary values just for init, could be maybe higher
MAX_SAMPLEFREQUENCY = 1_000_000
MAX_BLOCKSIZE = 2 ** 18
MAX_CHANNELS = 2
# REVIEW read by time instead by blocks

MAX_FEATURES = 4  # to increase them, the gui-design has to be updated!
OVERLAP = 0.5
ALARM_CHECK = 2  # ms
# ALARM_DELAY = 100  # number of blocks (higher number faster reading) # [ ] Read all during measurement only for replay?
ALARM_RESET = 3  # [s], if the score is in these interval below threshold -> alarm is resetted
ALARM_REALARM = 1000  # ms, retry to activate the alarm
ALARM_MAX_RETRYS = 20
# corresponding delay time: ALARM_DELAY * blocksize/samplefrequency

ALARMSETTINGS_TIPPS = [
    "to set no threshold for one feature of the channel, set the value to 0",
    "to set no threshold for all features for one channel, remove its channel number",
    "from the thresholds and the weighting_factors",
    "the channels to record is set with the measurement_settings.json!",
]

SMOOTH_DATA = False

DATA_SOURCE = "MQTT"  # "MQTT" or "DATABASE"
# if DATA_SOURCE is "DATABASE" -> MQTT_CONFIG is in the init overwritten to None
MQTT_CONFIG = {
    "broker_ip": "192.168.2.12",
    "broker_port": 1883,
    "timelive": 60,
}  # {"broker_ip": "192.168.102.109", "broker_port": 1883, "timelive": 60}

# [ ] TODO not saving data (tempfile which is going to be deleted) or writing to stream/buffer? -> BinaryIO?
# [ ] TODO rename the tabs and other element to increae the possiblity to understand which element is meant in the python code

# [x] TODO if starting a further measurement only the tradb is started but not the feature saving

# [ ] TODO store the timestamps of alarms (include which channel and features with treshold and actual level)
# [x] TODO add a button to reset the alarm
# [ ] TODO don't forget to set correct range (get the range with the mulichannel software -> edit config file)


class FileDialog(QDialog):
    def __init__(self, parent: QMainWindow, windowtitle: str, message: str, mode="save"):
        # [ ] Review variable type is not that specific, but MainWindow is declared later and it is not possible to declare SaveDialog later
        super().__init__()

        self.setWindowTitle(windowtitle)

        self.button_yes = QPushButton("Ja")
        self.button_no = QPushButton("Nein")

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.button_yes)
        buttonLayout.addWidget(self.button_no)
        # lambda function is needed to pass the SaveDialog object to close it in get_file_location
        self.button_yes.pressed.connect(lambda: parent.get_file_location(self, mode=mode))
        self.button_no.pressed.connect(self.close)  # do nothing if no is clicked

        self.layout = QVBoxLayout()
        message = QLabel(message)
        self.layout.addWidget(message)
        self.layout.addLayout(buttonLayout)
        self.setLayout(self.layout)


class MeasurementInterface(QMainWindow):
    def __init__(self):
        super(MeasurementInterface, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        saveFile = QAction("&Speicherort wählen", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip("Speicherort wählen")
        saveFile.triggered.connect(self.get_file_location)

        openHelp = QAction("&Hilfe aufrufen", self)
        openHelp.setShortcut("F1")  # [ ] Review standard key for help
        openHelp.setStatusTip("Hilfe aufrufen")
        # openHelp.triggered.connect() # TODO add here a Help page

        fileMenu = self.ui.menuSpeichern
        fileMenu.addAction(saveFile)
        helpMenu = self.ui.menuHilfe
        helpMenu.addAction(openHelp)

        self.outputfile_path = None
        self.configfile_path = CONFIGFILE_PATH
        self.alarmsettingsfile_path = ALARMSETTINGSFILE_PATH
        self.tradb_exist = False
        self.f = None
        self.trfdb = None
        self.trfdbfile = None
        self.last_alarm = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None}
        self.last_warning = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None}
        self.alarm_logfile = None
        self.alarm_entry = pd.DataFrame(
            columns=[
                "Absolute Timepoint",
                "Relative Timepoint",
                "Channel",
                "Feature",
                "Actual Value",
                "Threshold Value",
                "TRAI",
            ],
        )
        self.alarm_init = False
        self.alarm_retrys = 0
        self.first_alarm = True
        self.tradb = None
        self.last_plot_trai = 1
        self.last_alarm_trai = 1
        self.display_interval = DISPLAY_INTERVAL

        # QTimer
        self.alarm_timer = QtCore.QTimer()
        self.alarm_timer.timeout.connect(self.check_alarm)
        self.stop_measurement_timer = QtCore.QTimer()
        self.stop_measurement_timer.timeout.connect(self.stop_measurement)
        # self.progressBar_timer = QtCore.QTimer()
        # self.progressBar_timer.timeout.connect(self.update_progressbar)

        self.p_meas = None
        # [ ] TODO enable pridbwriting, if measuring with the fyrsonic (Visual AE desiered)
        # self.p_pridb = None
        self.p_trfdb = None
        self.replay = "no"

        self.display_measurement_settings()
        self.display_activated_channels()
        self.load_alarm_settings()

        self.init_alarm_feature_label()

        self.tabs_dynamic_plotters = []

        if DATA_SOURCE == "MQTT":
            self.mqtt_config = MQTT_CONFIG
            self.message_and_log("Starting the mqtt subscriber to the Machine Learning Models.")
            # [x] TODO add on message function
            self.client = init_mqtt(
                self.mqtt_config,
                mqtt_topics=["ml_data", "machine_meta", "machine_data", "user_meta", "user_data"],
                client_name="MeasurementGUI_ML_Subscriber",
                on_message_func=[
                    self.display_ml_output,
                    self.display_machine_meta_data,
                    self.display_machine_data,
                    self.display_event_meta_data,
                    self.display_event_data,
                ],
            )
        else:
            self.mqtt_config = None

        # self.event_loop = qasync.QEventLoop(self)
        self.init_feature_plots()
        self.init_spectrogram()

        # # tab 7: sensor inspection
        # self.ui.graphicsView_6.init_plot(
        #     color="b",
        #     display_interval=DISPLAY_INTERVAL,
        #     read_blocks=READ_BLOCKS,
        # )
        # self.tabs_dynamic_plotters.append(self.ui.graphicsView_4)
        # self.ui.comboBox.currentIndexChanged.connect(self.plot_timedata)

        self.ui.pushButton_2.pressed.connect(self.start_measurement)
        self.ui.pushButton.pressed.connect(self.stop_measurement)
        self.ui.pushButton_3.pressed.connect(self.replay_measurement)
        self.ui.pushButton_4.pressed.connect(self.stop_replay)
        self.ui.pushButton_5.pressed.connect(self.pause_replay)
        self.ui.set_Settings.pressed.connect(self.set_settings)
        self.ui.tabWidget.tabBarClicked.connect(self.get_which_tab)
        self.ui.pushButton_overwrite_classification.pressed.connect(self.reset_alarm_state)

        # background/ state of the sensors
        self.reset_alarm_state()

        self.ui.dateTimeEdit_metatimestamp.setDateTime(datetime.now())
        self.ui.dateTimeEdit_eventtimestamp.setDateTime(datetime.now())

    def get_read_blocks(self) -> Union[int, None]:
        """Get the number of blocks to read
        replaying measurement -> simulating feature data stream with the correct velocity
        not replaying measurement -> read all available data
        """
        if self.replay == "active":
            # default -> blockduration: 20 ms
            # read_blocks = nr_channels * DISPLAY_INTERVAL/blockduration
            read_blocks = 30  # max. number of blocks to read at once (for plotting)
        else:
            read_blocks = None
        return read_blocks

    def get_read_query(self, last_trai: int) -> str:
        """Get the read query with a limit of blocks to read in replay mode or without limit during measurement

        Args:
            last_trai(int): last trai from the previous read task

        Returns:
            str: query to read data from tradb or trfdb
        """
        read_blocks = self.get_read_blocks()
        if read_blocks:
            query = f"trai >= {last_trai} AND trai < {last_trai + read_blocks}"
        else:
            query = f"trai >= {last_trai}"
        return query

    def init_spectrogram(self) -> None:
        """Initialize the spectrogram"""

        read_blocks = self.get_read_blocks()
        # tab 6: spectrogram
        self.ui.graphicsView_5.init_plotwindow(
            display_interval=DISPLAY_INTERVAL / 2,
            read_blocks=read_blocks,
        )
        self.spectrogram_plotter = self.ui.graphicsView_5

        self.ui.comboBox_2.currentIndexChanged.connect(self.plot_spectrogram)

    # @qasync.asyncSlot()
    def init_feature_plots(self) -> None:
        """Initialize the feature plots: feature name in the datasource, for the label, unit of the feature"""
        # [ ] REVIEW units of the DynamicFeaturePlotter!
        sources = ["Invalid"] * MAX_FEATURES
        ylabels = ["None"] * MAX_FEATURES
        units = ["V"] * MAX_FEATURES
        read_blocks = self.get_read_blocks()

        self.tabs_dynamic_plotters = []

        for i, feature in enumerate(self.features):
            sources[i] = feature
            ylabels[i] = feature
            units[i] = self.features_units[feature]

        # tab 2: Amplitude plot
        self.ui.graphicsView.init_plot(
            sources[0],
            ylabels[0],
            unit=units[0],
            display_interval=DISPLAY_INTERVAL,
            read_blocks=read_blocks,
            smooth_data=SMOOTH_DATA,
            mqtt_config=self.mqtt_config,
            # event_loop=self.event_loop,
        )
        self.tabs_dynamic_plotters.append(self.ui.graphicsView)

        # tab 3: RMS plot
        self.ui.graphicsView_2.init_plot(
            sources[1],
            ylabels[1],
            unit=units[1],
            display_interval=DISPLAY_INTERVAL,
            read_blocks=read_blocks,
            smooth_data=SMOOTH_DATA,
            mqtt_config=self.mqtt_config,
        )
        self.tabs_dynamic_plotters.append(self.ui.graphicsView_2)

        # tab 4: HFC plot
        self.ui.graphicsView_3.init_plot(
            sources[2],
            ylabels[2],
            unit=units[2],
            display_interval=DISPLAY_INTERVAL,
            read_blocks=read_blocks,
            smooth_data=SMOOTH_DATA,
            mqtt_config=self.mqtt_config,
        )
        self.tabs_dynamic_plotters.append(self.ui.graphicsView_3)

        # tab 5: Energy plot
        self.ui.graphicsView_4.init_plot(
            sources[3],
            ylabels[3],
            unit=units[3],
            display_interval=DISPLAY_INTERVAL,
            read_blocks=read_blocks,
            smooth_data=SMOOTH_DATA,
            mqtt_config=self.mqtt_config,
        )
        self.tabs_dynamic_plotters.append(self.ui.graphicsView_4)
        # # spectrogram
        # self.ui.graphicsView_6.init_plot(
        #     sources[0],
        #     ylabels[0],
        #     unit=units[0],
        #     display_interval=DISPLAY_INTERVAL,
        #     read_blocks=read_blocks,
        #     smooth_data=SMOOTH_DATA,
        # )
        self.tabs_dynamic_plotters.append(self.ui.graphicsView)

    def init_alarm_feature_label(self) -> None:
        """Initialize (Renames) the feature labels in the settings tab for thresholds, for tab names and in the legend of the plots"""
        # [ ] TODO optional: Add option change features during execution?
        alarm_labels = [self.ui.label_30, self.ui.label_29, self.ui.label_28, self.ui.label_38]
        # x[0] the temporarly created column, has the name 0
        pd.DataFrame(range(len(alarm_labels))).apply(
            lambda x: alarm_labels[x.name].setText(f"Feature {x.name + 1}"), axis=1
        )  # if there not MAX_Features in the alarm_settings the remaining features are set to default names
        pd.DataFrame(self.alarm_features).apply(lambda x: alarm_labels[x.name].setText(x[0]), axis=1)

        display_texts = [f"Feature{i+1}" for i in range(MAX_FEATURES)]

        # rename the feature tabs
        for i, feature in enumerate(self.features):
            display_texts[i] = feature
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_2), display_texts[0])
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_5), display_texts[1])
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_6), display_texts[2])
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_7), display_texts[3])

    def message(self, s: str) -> None:
        """Display log messages

        Args:
            s (str): log message
        """
        # if passing the log-message here to the LOGGER, there are duplicate entries for child logs
        # [x] TODO add logging to file!
        self.ui.plainTextEdit.appendPlainText(s)
        # [ ] REVIEW this LOGGER is unnecessary generate duplicate entries
        # LOGGER.info(s)

    def message_and_log(self, s: str) -> None:
        """Use this function to print log messages in the message filed and pass them to logging

        Args:
            s (str): log message
        """
        self.message(s)
        LOGGER.info(s)

    def start_measurement(self):
        # [ ] @KB TODO stopping of the measurement!
        # [ ] TODO the feature saving is not always working
        self.load_alarm_settings()
        if not self.outputfile_path:
            dlg = FileDialog(
                self,
                "Speichern ?",
                "Sollen die Messdaten gespeichert werden?",
                mode="save",
            )
            dlg.exec()

        if self.outputfile_path:

            if not self.p_meas or self.p_meas.state() == QtCore.QProcess.NotRunning:  # no process running
                # self.ui.checkBox_8.setDisabled(True)
                self.restart_plotting()
                self.reset_alarm_state()
                # [ ] TODO setDisable alle Einstellungen (alle Checkboxes, ..)
                # self.check_trfdb.setDisabled(True)
                self.message_and_log(f"Using following measurement configuration: {self.configfile_path}")
                self.message_and_log(f"Writing data to: {self.outputfile_path}")
                self.message_and_log("Starting measurement script.")
                self.p_meas = QtCore.QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
                self.p_meas.readyReadStandardOutput.connect(lambda: self.handle_stdout(self.p_meas))
                self.p_meas.readyReadStandardError.connect(lambda: self.handle_stderr(self.p_meas))
                self.p_meas.stateChanged.connect(lambda state: self.handle_state(state, "Measurement"))
                # [ ] TODO add option to decide between condition wave or TiePie
                # [ ] TODO later add option to start tiepie and conditionWave from one gui
                # [ ] Review is that style okay?
                measurementinterface_script = PurePath(inspect.getsourcefile(measurement_interface))
                self.p_meas.start(
                    str(PYTHON_VENV),
                    [
                        str(measurementinterface_script),
                        "-o " + str(self.outputfile_path),
                        "-c " + str(self.configfile_path),
                    ],
                )
                # if self.check_pridb.isChecked():
                #     self.message_and_log("Pridb geneation is activated.")
                #     self.start_pridb_writer()

                # if self.ui.checkBox_8.isChecked():
                self.message_and_log("Feature data are stored.")
                QtCore.QTimer.singleShot(5000, self.start_trfdb_writer)
                self.alarm_init = False
            else:
                self.message_and_log("Measurement script is running please wait.")

            # self.timer.start(self.display_interval)
        else:
            self.message_and_log("No valid location to save the data provied.")
            self.message_and_log("Can not start a measurement.")

    def stop_measurement(self):
        if self.p_meas:
            if self.p_meas.state() == QtCore.QProcess.Running:
                self.message_and_log("Stopping measurement.")
                pid = self.p_meas.processId()
                LOGGER.debug(f"Measurement process id: {pid}")
                if os.name == "nt":  # windows machine
                    # for _ in range(5):
                    try:
                        os.kill(pid, signal.CTRL_C_EVENT)  # CTRL-C on windows machines
                        # kill signal send to other python processes also?
                        # time.sleep(0.75)
                        self.stop_measurement_timer.start(250)  # check if terminated in 250 ms
                    except PermissionError:
                        pass
                        # continue
                    except KeyboardInterrupt:
                        #     # not sure why the KeyboardInterrupt is recogniced here (should only send to the measurement script)
                        pass
                        # continue
                else:
                    # for _ in range(5):
                    try:
                        os.kill(pid, signal.SIGINT)  # SIGINT is CTRL-C (linux machines)
                        # time.sleep(0.75)
                        self.stop_measurement_timer.start(250)
                    except PermissionError:
                        pass
                        # continue
                    except KeyboardInterrupt:
                        pass
                        # continue
                stop = datetime.now()
                stop_str = stop.strftime("%Y_%m_%d_%H_%M_%S.%f")
                LOGGER.debug(f"Last tradb stop signal send at: {stop_str}")
                self.p_meas.waitForFinished(5000)
                self.p_meas.finished.connect(lambda: self.message_and_log("Measurement process finished."))
                self.outputfile_path = None
                self.trfdbfile = None
            # self.p_meas = None
            # self.p_pridb.waitForFinished(5000)
            # self.p_pridb = None
        else:
            self.stop_measurement_timer.stop()
        if self.p_trfdb:
            if self.p_trfdb.state() == QtCore.QProcess.Running:
                self.p_trfdb.waitForFinished(5000)
                self.p_trfdb.finished.connect(lambda: self.message_and_log("Feature process finished."))
                # self.p_trfdb = None
                # self.ui.checkBox_8.setDisabled(False)
        self.alarm_timer.stop()
        # self.check_trfdb.setDisabled(False)
        # self.timer.stop()

    def start_pridb_writer(self):
        if not self.p_pridb:  # no process running
            self.message_and_log("Starting pridb writer script.")
            self.p_pridb = QtCore.QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p_pridb.readyReadStandardOutput.connect(lambda: self.handle_stdout(self.p_pridb))
            self.p_pridb.readyReadStandardError.connect(lambda: self.handle_stderr(self.p_pridb))
            self.p_pridb.stateChanged.connect(lambda state: self.handle_state(state, "Pridb writer"))
            self.p_pridb.start(
                str(PYTHON_VENV),
                [str(Path(r"src\pytiepiesql\measurement\pridb_writer.py").absolute())],
            )
        else:
            self.message_and_log("Pridb writer script is running please wait.")

    def start_trfdb_writer(self):
        if not self.p_trfdb or self.p_trfdb.state() == QtCore.QProcess.NotRunning:  # no process running
            self.message_and_log("Starting trfdb writer script.")
            self.p_trfdb = QtCore.QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.p_trfdb.readyReadStandardOutput.connect(lambda: self.handle_stdout(self.p_trfdb))
            self.p_trfdb.readyReadStandardError.connect(lambda: self.handle_stderr(self.p_trfdb))
            self.p_trfdb.stateChanged.connect(lambda state: self.handle_state(state, "Trfdb writer"))
            trfdb_writer_script = PurePath(inspect.getsourcefile(trfdb_writer))
            # the outputfile_path (tradb) is the inputfile for the trfdb-writer
            if not self.mqtt_config:
                self.p_trfdb.start(
                    str(PYTHON_VENV),
                    [
                        str(trfdb_writer_script),
                        "-i " + str(self.outputfile_path),
                        "-f " + (", ").join(self.features),
                    ],
                )

                self.trfdbfile = PurePath(self.outputfile_path.parent, self.outputfile_path.stem + ".trfdb")
                self.alarm_timer.start(5000)  # start alarm after 5 s after trfdb creation
            else:
                # [ ] REVIEW automaticly not saving feature data if using mqtt
                # [ ] TODO passing the other mqtt configs
                self.p_trfdb.start(
                    str(PYTHON_VENV),
                    [
                        str(trfdb_writer_script),
                        "-i " + str(self.outputfile_path),
                        "-f " + (", ").join(self.features),
                        "-s " + "False",
                        "-b " + str(self.mqtt_config["broker_ip"]),
                        "-p " + str(self.mqtt_config["broker_port"]),
                    ],
                )
        else:
            self.message_and_log("Trfdb writer script is running please wait.")

    # def stop_pridb_writer(self):
    #     if self.p_pridb:
    #         self.message_and_log("Stopping pridb writer.")
    #         self.p_pridb.terminate()

    def get_which_tab(self, tabIndex: int) -> None:
        # [ ] Review if measurement should be done set settings should be clicked
        # [ ] Review in Replay-mode the settings are read always the tab is switched (overhead?)

        # [ ] TODO if not saving the features, disable the feature view (not possible)
        if not DATA_SOURCE == "MQTT":
            for i in self.tabs_dynamic_plotters:
                if i.last_trai > self.last_plot_trai:
                    self.last_plot_trai = i.last_trai
            if self.last_plot_trai < self.spectrogram_plotter.last_trai:
                self.last_plot_trai = self.spectrogram_plotter.last_trai

        if tabIndex > 0 and tabIndex < 5:
            # feature tabs
            self.plot_featuredata(tabIndex)
            # [ ] TODO uncomment that line if the tab sensor inspection should be used
            # self.tabs_dynamic_plotters[4].stop_update_routine()
            self.spectrogram_plotter.stop_update_routine()
        elif tabIndex == 5:
            # spectrogram tab
            self.plot_spectrogram(0)
            for dynamic_plotter_tab in self.tabs_dynamic_plotters:
                dynamic_plotter_tab.stop_update_routine()
        # elif tabIndex == 6:
        #     # channel = self.ui.comboBox.currentIndex() + 1
        #     # sensor inspection tab
        #     self.plot_timedata(0)
        #     for i in range(4):
        #         self.tabs_dynamic_plotters[i].stop_update_routine()
        #     # if self.trfdb:
        #     #     self.trfdb.close()
        #     self.spectrogram_plotter.stop_update_routine()
        else:
            self.spectrogram_plotter.stop_update_routine()
            for dynamic_plotter_tab in self.tabs_dynamic_plotters:
                dynamic_plotter_tab.stop_update_routine()

    def plot_featuredata(self, index: int) -> None:
        if not self.replay in ["pause", "stopp"]:
            if not DATA_SOURCE == "MQTT" and self.trfdbfile:
                if not self.trfdb:
                    self.trfdb = vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro")
                elif not self.trfdb.connected:
                    self.trfdb = vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro")

                query = self.get_read_query(self.last_plot_trai)
                # [ ] Review using last plot trai for all plots
                datagenerator = self.trfdb.iread(query_filter=query)
                self.tabs_dynamic_plotters[index - 1].start_update_routine(datagenerator, self.active_channels)
            elif DATA_SOURCE == "MQTT":
                self.tabs_dynamic_plotters[index - 1].start_update_routine(None, self.active_channels)
            else:
                self.message_and_log("Can't plot anything without an feature database.")

    def plot_timedata(self, _) -> None:
        # [ ] TODO implement the display of the feature values in this window
        # maybe only the max. value in a certain time interval, should be readable
        if not self.replay in ["pause", "stopp"]:
            if self.outputfile_path:
                if not self.tradb:
                    self.tradb = vae.io.TraDatabase(filename=self.outputfile_path, mode="ro")
                elif not self.tradb.connected:
                    self.tradb = vae.io.TraDatabase(filename=self.outputfile_path, mode="ro")
                # the last trai has to update here as well, for switching the sensors to plot within that tab
                if self.tabs_dynamic_plotters[4].last_trai > self.last_plot_trai:
                    self.last_plot_trai = self.tabs_dynamic_plotters[4].last_trai
                query = self.get_read_query()
                # [ ] Review using last plot trai for all plots
                datagenerator = self.tradb.iread(query_filter=query)
                channel = self.ui.comboBox.currentIndex() + 1
                self.tabs_dynamic_plotters[4].start_update_routine(datagenerator, channel)
            else:
                self.message_and_log("Can't plot anything without an transient database.")

    def plot_spectrogram(self, _) -> None:
        if not self.replay in ["pause", "stopp"]:
            if self.outputfile_path:
                if not self.tradb:
                    self.tradb = vae.io.TraDatabase(filename=self.outputfile_path, mode="ro")
                elif not self.tradb.connected:
                    self.tradb = vae.io.TraDatabase(filename=self.outputfile_path, mode="ro")
                # the last trai has to update here as well, for switching the sensors to plot within that tab
                if self.spectrogram_plotter.last_trai > self.last_plot_trai:
                    self.last_plot_trai = self.spectrogram_plotter.last_trai
                query = self.get_read_query(self.last_plot_trai)
                # [ ] Review using last plot trai for all plots
                datagenerator = self.tradb.iread(query_filter=query)
                channel = self.ui.comboBox_2.currentIndex() + 1
                self.spectrogram_plotter.start_update_routine(datagenerator, channel, overlap=OVERLAP)
            else:
                self.message_and_log("Can't plot anything without an transient database.")

    def handle_stderr(self, process: QtCore.QProcess):
        # logging prints to stderr per default
        try:
            data = process.readAllStandardError()
            stderr = bytes(data).decode("utf8")
            LOGGER.info(stderr)
        except KeyboardInterrupt:
            # sometimes the KeyoardInterrupt to stop the measurement is catched here?
            pass

    def handle_stdout(self, process: QtCore.QProcess):
        try:
            data = process.readAllStandardOutput()
            stdout = bytes(data).decode("utf8")
            LOGGER.info(stdout)
        except KeyboardInterrupt:
            pass

    def handle_state(self, state, process_name: str):
        # [x] TODO maybe add a constant light of the process state
        states = {
            QtCore.QProcess.NotRunning: "Not running",
            QtCore.QProcess.Starting: "Starting",
            QtCore.QProcess.Running: "Running",
        }
        state_name = states[state]
        if process_name == "Measurement":
            if state_name == "Not running":
                self.stop_measurement_timer.stop()
        if process_name == "Trfdb writer":
            if state_name in ["Starting", "Running"]:
                self.display_active_measurement()
            else:
                self.reset_alarm_state()
                # self.ui.progressBar.setValue(0)
                # self.progressBar_timer.stop()
                # self.ui.Process_name.setText(None)
        self.message_and_log(f"{process_name} State changed: {state_name}")

    def get_file_location(self, filedialog: Optional[FileDialog] = None, mode: str = "save", attempt: int = 0) -> None:

        if filedialog:
            filedialog.close()
        if mode == "save":
            # [ ] TODO fix the default directory opening correctly
            name = QFileDialog.getSaveFileName(
                self,
                "Messung abspeichern",
                directory="data/Measurements",
                filter="Feature-Databases (*.trfdb)",
            )
        else:
            name = QFileDialog.getOpenFileName(
                self,
                "Messung auswählen",
                directory="data/Measurements",
                filter="Feature-Databases (*.trfdb)",
            )
        if name[0]:
            self.outputfile_path = PurePath(name[0])
            self.set_filehandler()
            self.trfdbfile = PurePath(self.outputfile_path.parent, self.outputfile_path.stem + ".trfdb")
            # self.alarm_logfile = PurePath(self.outputfile_path.parent, self.outputfile_path.stem + ".csv")
            # self.alarm_logfile_handler = FileHandler(filename=self.alarm_logfile.name, wkd=self.alarm_logfile.parent)
        else:
            attempt += 1
            if attempt < 4:
                self.get_file_location(filedialog, mode, attempt)
            else:
                self.message_and_log("4 attemps to set the featuredatabase for saving failed.")
                # [ ] TODO break here? Okay like this

    def set_filehandler(self) -> None:
        if self.outputfile_path:
            wkd = self.outputfile_path.parent
            filename = f"{self.outputfile_path.stem}.tradb"
            self.f = FileHandler(filename=filename, wkd=wkd)
            self.outputfile_path = self.f.current_file.path
        if self.f.exist_file() and self.replay == "no":
            now = datetime.now()
            now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
            self.f.set_file(f"{self.outputfile_path.stem}_{now_str}.tradb")
            self.outputfile_path = self.f.current_file.path
            # self.tradb_exist = True

    def get_settings(self) -> None:
        self.get_activated_channels()
        self.get_alarm_thresholds()
        self.get_filter_settings()

    def set_settings(self) -> None:
        # [x] TODO set all settings not editable during measurement?
        # to make the settings effective Einstellungen übernehmen has to be clicked
        self.get_settings()
        self.write_settings_to_configfile()
        self.write_alarm_settings()

    def get_activated_channels(self) -> None:
        """gets the activated channels from the gui"""
        # checkout the ui file with qt-designer to get the elment names
        # click in the graphic window on the element -> in the Object view is now the variable name selected

        self.active_channels = []

        if not self.replay == "active":

            for i, sens_btn in enumerate(
                [
                    self.ui.checkBox,
                    self.ui.checkBox_2,
                    self.ui.checkBox_4,
                ]
            ):
                if i == 0 and sens_btn.isChecked():
                    self.active_channels = list(range(1, 7))
                    break
                elif sens_btn.isChecked():
                    self.active_channels.append(i)
        else:
            try:
                with vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro") as trfdb:
                    # reading of only the MAX channels would be sufficent
                    records = trfdb.read(query_filter=f"trai >= 1 AND trai <= {2*MAX_CHANNELS}")
                    self.active_channels = records["Channel"].unique().tolist()
            except sqlite3.OperationalError:
                self.message_and_log("Can not connect to the feature database. Replay mode not possible.")
                self.message_and_log("Please check the path to the feature database.")

    def display_activated_channels(self) -> None:
        """Displays the activated channels in the gui"""
        # [ ] REVIEW the activated channels for the measurement are used if they differ from the channels in the alarm_settings
        # all channels ->  self.ui.checkBox,
        channel_boxes = [
            self.ui.checkBox_2,
            self.ui.checkBox_4,
        ]
        # uncheck all channels
        pd.Series(range(MAX_CHANNELS + 1)).apply(lambda x: channel_boxes[x - 1].setChecked(False))

        active_channels_ser = pd.Series(self.active_channels)
        active_channels_ser.apply(lambda x: channel_boxes[x - 1].setChecked(True))

    def get_alarm_thresholds(self) -> None:
        """Gets the alarm thresholds from the gui"""

        # checkout the ui file with qt-designer to get the elment names
        # [ ] Rename the elements with qt-designer to get the needed names straightforward
        # [x] TODO implement that flexible
        self.alarm_thresholds = pd.DataFrame()
        # first feature (amplitude)
        self.alarm_thresholds[self.ui.label_30.text()] = pd.Series(
            [
                self.ui.doubleSpinBox.value(),
                self.ui.doubleSpinBox_2.value(),
            ]
        )
        # second feature (RMS)
        self.alarm_thresholds[self.ui.label_29.text()] = pd.Series(
            [
                self.ui.doubleSpinBox_7.value(),
                self.ui.doubleSpinBox_8.value(),
            ]
        )

        # third feature (Hochfrequenter Anteil)
        self.alarm_thresholds[self.ui.label_28.text()] = pd.Series(
            [
                self.ui.doubleSpinBox_13.value(),
                self.ui.doubleSpinBox_14.value(),
            ]
        )

        # 4th feature (Energie)
        self.alarm_thresholds[self.ui.label_38.text()] = pd.Series(
            [
                self.ui.doubleSpinBox_19.value(),
                self.ui.doubleSpinBox_20.value(),
            ]
        )
        self.alarm_thresholds.index = np.arange(1, self.alarm_thresholds.shape[0] + 1)
        self.alarm_thresholds.index = self.alarm_thresholds.index.rename("Channel")
        # self.alarm_thresholds = self.alarm_thresholds.rename(
        #     columns={
        #         old_name: new_name for new_name, old_name in zip(self.alarm_features, self.alarm_thresholds.columns)
        #     }
        # )
        self.alarm_thresholds = self.alarm_thresholds.loc[self.alarm_thresholds.index.isin(self.active_channels)]

    def display_alarm_thresholds(self) -> None:
        """Displays the current alarm thresholds in the gui"""
        # [ ] Review two small values like 1e-8 (HFC) is set to 0
        # [ ] REVIEW if there less than MAX_FEATURES in self.alarm_features, the remaining boxes are set to 0
        # checkout the ui file with qt-designer to get the elment names
        # [ ] Rename the elements with qt-designer to get the needed names straightforward
        # first feature (amplitude)
        alarm_thresh_spin_boxes = [
            self.ui.doubleSpinBox,
            self.ui.doubleSpinBox_2,
        ]
        if len(self.alarm_features) > 0:
            if self.alarm_features[0] in self.alarm_thresholds.columns:
                display_df = self.alarm_thresholds[self.alarm_features[0]].to_frame()
        else:
            display_df = pd.DataFrame([0] * len(alarm_thresh_spin_boxes))
        # to frame() is needed to access the index, see: https://stackoverflow.com/a/47645833
        display_df.apply(lambda x: alarm_thresh_spin_boxes[x.name - 1].setValue(x), axis=1)

        # second feature (RMS)
        alarm_thresh_spin_boxes = [
            self.ui.doubleSpinBox_7,
            self.ui.doubleSpinBox_8,
        ]
        if len(self.alarm_features) > 1:
            if self.alarm_features[1] in self.alarm_thresholds.columns:
                display_df = self.alarm_thresholds[self.alarm_features[1]].to_frame()
        else:
            display_df = pd.DataFrame([0] * len(alarm_thresh_spin_boxes))

        self.alarm_thresholds[self.alarm_features[1]].to_frame().apply(
            lambda x: alarm_thresh_spin_boxes[x.name - 1].setValue(x), axis=1
        )

        # third feature (Hochfrequenter Anteil)
        alarm_thresh_spin_boxes = [
            self.ui.doubleSpinBox_13,
            self.ui.doubleSpinBox_14,
        ]
        if len(self.alarm_features) > 2:
            if self.alarm_features[2] in self.alarm_thresholds.columns:
                display_df = self.alarm_thresholds[self.alarm_features[2]].to_frame()
        else:
            display_df = pd.DataFrame([0] * len(alarm_thresh_spin_boxes))
        display_df.apply(lambda x: alarm_thresh_spin_boxes[x.name - 1].setValue(x), axis=1)

        # 4th feature (Energie)
        alarm_thresh_spin_boxes = [
            self.ui.doubleSpinBox_19,
            self.ui.doubleSpinBox_20,
        ]
        if len(self.alarm_features) > 3:
            if self.alarm_features[3] in self.alarm_thresholds.columns:
                display_df = self.alarm_thresholds[self.alarm_features[3]].to_frame()
        else:
            display_df = pd.DataFrame([0] * len(alarm_thresh_spin_boxes))
        display_df.apply(lambda x: alarm_thresh_spin_boxes[x.name - 1].setValue(x), axis=1)

    def get_filter_settings(self) -> None:

        # checkout the ui file with qt-designer to get the elment names
        # lower cut-off frequency
        # [ ] TODO rewrite the reading corresponding the alarm settings read in
        lower_cut_freq = {}
        for i, setting in enumerate(
            [
                self.ui.spinBox,
                self.ui.spinBox_2,
            ],
            1,
        ):
            lower_cut_freq[i] = setting.value()

        # upper cut-off frequency
        upper_cut_freq = {}
        for i, setting in enumerate(
            [
                self.ui.spinBox_7,
                self.ui.spinBox_8,
            ],
            1,
        ):
            upper_cut_freq[i] = setting.value()

        self.filter_settings = pd.DataFrame()
        self.filter_settings["Highpass Filter Cutoff Frequency"] = pd.Series(lower_cut_freq)
        self.filter_settings["Lowpass Filter Cutoff Frequency"] = pd.Series(upper_cut_freq)

    def write_settings_to_configfile(self) -> None:

        if len(self.active_channels) > 0:
            f = FileHandler(filename=self.configfile_path.name, wkd=self.configfile_path.parent)
            settings = f.read()
            device = settings.pop("Device")
            settings_df = pd.DataFrame().from_records(settings)
            # drop all no active channels from the measurement configfile
            settings_df_temp = settings_df.drop(
                settings_df[~settings_df.Channel.isin(self.active_channels + ["[-]"])].index
            )
            if not settings_df_temp.shape[0] > 1:
                settings_df = settings_df.iloc[0:2, :]
                settings_df.loc[1, "Channel"] = self.active_channels[0]
                # [ ] TODO add the channel description possibility
                settings_df.loc[1, "Channel Description"] = f"Sensor {self.active_channels[0]}"
            else:
                settings_df = settings_df_temp
            # add active channels to the measurement configfile
            for ch in self.active_channels:
                # use here values otherwise the index is checked
                if not ch in settings_df["Channel"].values:
                    new_row = settings_df.iloc[-1].copy()  # copy is here needed to not updated the original data
                    new_row["Channel"] = ch
                    new_row["Channel Description"] = f"Sensor {ch}"
                    settings_df = settings_df.append(new_row)
            settings_df = settings_df.reset_index(
                drop=True
            )  # this line is need, otherwise the following changes are not always made!
            settings_df.loc[
                settings_df["Channel"].isin(self.active_channels),
                "Highpass Filter Cutoff Frequency",
            ] = self.filter_settings.loc[self.active_channels, "Highpass Filter Cutoff Frequency"].values
            settings_df.loc[
                settings_df["Channel"].isin(self.active_channels),
                "Lowpass Filter Cutoff Frequency",
            ] = self.filter_settings.loc[self.active_channels, "Lowpass Filter Cutoff Frequency"].values
            settings_df.loc[self.active_channels[0], "Additional Text"] = self.ui.lineEdit_13.text()
            settings = settings_df.to_dict("list")
            settings["Device"] = device
            f.write(settings)
        else:
            self.message_and_log("You have to activate sensors before you can set the settings.")

    def load_measurement_settings(self) -> pd.DataFrame:
        """Loads the measurement settings from the data\settings\measurement_settings.json or in replay mode
        reads the measurement settings from the database

        The active channels are also determined.

        Returns:
            pd.DataFrame: measurement settings
        """
        if not self.replay == "active":
            f = FileHandler(filename=self.configfile_path.name, wkd=self.configfile_path.parent)
            settings = f.read()
            _ = settings.pop("Device")
            settings_df = pd.DataFrame().from_records(settings)
        else:
            try:
                settings_df = read_acq_settings(self.trfdbfile)
            except sqlite3.OperationalError:
                self.message_and_log(
                    "Can not connect to the feature database. Reading of the acquisition settings is not possible."
                )
                self.message_and_log("Please check the path to the feature database.")

        self.active_channels = settings_df.loc[1:, "Channel"].to_list()
        return settings_df

    def display_measurement_settings(self) -> None:
        """Displays the measurement settings in the gui.
        Displayed values: Filter frequencies and the aditional infos.
        """
        # [x] TODO display the current settings from the config file
        # [x] TODO add read and save of the alarm configs!

        settings_df = self.load_measurement_settings()

        # lower cut off frequencies
        lower_cut_freq_boxes = [
            self.ui.spinBox,
            self.ui.spinBox_2,
        ]
        lower_cut_freq = settings_df.loc[1:, "Highpass Filter Cutoff Frequency"]
        lower_cut_freq = pd.to_numeric(lower_cut_freq, errors="coerce")
        lower_cut_freq = lower_cut_freq.fillna(0.0)
        # upper cut off frequencies
        upper_cut_freq_boxes = [
            self.ui.spinBox_7,
            self.ui.spinBox_8,
        ]
        upper_cut_freq = settings_df.loc[1:, "Lowpass Filter Cutoff Frequency"]
        upper_cut_freq = pd.to_numeric(upper_cut_freq, errors="coerce")
        upper_cut_freq = upper_cut_freq.fillna(0.0)

        cut_freq = pd.Series(
            index=range(1, len(lower_cut_freq_boxes) + 1), data=[0] * len(lower_cut_freq_boxes)
        )  # init with 0
        # all values not in settings_df are filled with 0 from cut_freq
        disp_values_high = upper_cut_freq.combine_first(cut_freq)
        disp_values_low = lower_cut_freq.combine_first(cut_freq)
        # to frame() is needed to access the index, see: https://stackoverflow.com/a/47645833
        disp_values_high.to_frame().apply(lambda x: upper_cut_freq_boxes[x.name - 1].setValue(int(x)), axis=1)
        disp_values_low.to_frame().apply(lambda x: lower_cut_freq_boxes[x.name - 1].setValue(int(x)), axis=1)

        if not settings_df.loc[1:, "Additional Text"].isna().all():
            # [ ] TODO select all not None/nan/Null text
            # add_text = settings_df.loc[settings_df.loc[1:, "Additional Text"].isna(), "Additional Text"]
            self.ui.lineEdit_13.setText((" ").join(settings_df.loc[1:, "Additional Text"].astype(str)).strip())
        self.display_activated_channels()

    def replay_measurement(self) -> None:
        """Replay the measurement data from a db file."""
        # [ ] REVIEW it is not possible to review a message if the data is transferred via MQTT
        # [ ] TODO get the state if the measurement is over -> new init the replay
        if not self.replay == "pause":
            self.replay = "active"  # is checked in get_file_location
            self.get_file_location(None, mode="open")
            if self.outputfile_path:
                self.get_activated_channels()
                self.display_measurement_settings()
                self.load_alarm_settings()
                self.restart_plotting()
                self.reset_alarm_state()
                self.message_and_log("Replay mode: start")
                self.alarm_timer.start(ALARM_CHECK)
                self.alarm_init = False
            else:
                self.replay == "no"
        else:
            self.replay = "active"
            self.message_and_log("Replay mode: Go on.")

        self.alarm_timer.start(ALARM_CHECK)

    def pause_replay(self) -> None:
        self.replay = "pause"
        self.alarm_timer.stop()
        self.stop_plotting()
        self.message_and_log("Replay mode: pause")

    def stop_replay(self) -> None:
        self.replay = "stopp"
        self.outputfile_path = None
        self.trfdbfile = None
        self.alarm_timer.stop()
        self.stop_plotting()
        # self.restart_plotting()
        self.message_and_log("Replay mode: stop")
        self.restart_plotting()

    def restart_plotting(self) -> None:
        # [ ] Review if restart measurement to same file
        self.last_alarm_trai = 1
        self.last_plot_trai = 1
        for i in self.tabs_dynamic_plotters:
            i.reset_plot()

        self.spectrogram_plotter.reset_plot()

        self.init_feature_plots()
        self.init_spectrogram()
        self.trfdb = None
        self.tradb = None

    def stop_plotting(self) -> None:
        for plotter in self.tabs_dynamic_plotters:
            plotter.stop_update_routine()
        self.spectrogram_plotter.stop_update_routine()
        if self.trfdb:
            self.trfdb.close()
        if self.tradb:
            self.tradb.close()

    def reset_alarm_state(self) -> None:
        """Resets the alarm state of all possible sensors in the GUI

        The background colour is set to None (Grey).
        """
        for ch in range(1, 7):
            self.change_channel_background(ch, None)

    def display_active_measurement(self) -> None:
        """Sets the background color of active channels to green
        This is an indicator, that the measurement is working/active.
        """
        # [ ] REVIEW display only channels with alarm thresholds set? and other color for measuring?
        for ch in self.active_channels:
            self.change_channel_background(ch, "green")

    def display_ml_output(self, message: Dict) -> None:
        """On new messages to the ml topic these function is called and the new message is evaluated"""
        # [ ] TODO go on
        timestamp = datetime.strptime(message["timestamp"], TIMESTAMP_FORMAT)
        pass

    def display_machine_meta_data(self, message: Dict) -> None:
        for key, value in message.items():
            self.ui.plainTextEdit_machinemetadata.appendPlainText(f"{key}: {value}")

    def display_event_meta_data(self, message: Dict) -> None:
        # [ ] TODO go on
        for key, value in message.items():
            self.ui.plainTextEdit_eventmetadata.appendPlainText(f"{key}: {value}")

    def display_event_data(self, message: Dict) -> None:
        """Displays the event data

        Args:
            message (Dict): keys: "timestamp", "event"
        """
        timestamp = datetime.strptime(message["timestamp"], TIMESTAMP_FORMAT)
        self.ui.dateTimeEdit_eventtimestamp.setDateTime(timestamp)
        self.ui.label_event.setText(message["event"])

    def display_machine_data(self, message: Dict) -> None:
        """Displays the machine (meta) data

        Args:
            message (Dict): keys: velocity, greasing, cooling, material, old_diameter, new_diameter, timestamp
        """
        timestamp = datetime.strptime(message["timestamp"], TIMESTAMP_FORMAT)
        self.ui.doubleSpinBox_velocity.setValue(message["velocity"])
        if message["greasing"]:
            self.ui.comboBox_greasing.setCurrentIndex(0)
        else:
            self.ui.comboBox_greasing.setCurrentIndex(1)
        if message["cooling"]:
            self.ui.comboBox_cooling.setCurrentIndex(0)
        else:
            self.ui.comboBox_cooling.setCurrentIndex(1)
        if message["material"] == "Federstahl":
            self.ui.comboBox_material.setCurrentIndex(0)
        elif message["material"] == "Baustahl":
            self.ui.comboBox_material.setCurrentIndex(1)
        else:
            self.ui.comboBox_material.setCurrentIndex(2)
        self.ui.doubleSpinBox_old_diameter.setValue(message["old_diameter"])
        self.ui.doubleSpinBox_new_diameter.setValue(message["new_diameter"])
        self.ui.dateTimeEdit_metatimestamp.setDateTime(timestamp)

    def init_alarm(self) -> None:
        """Initialize the alarm
        Check if any thresholds are set and if the feature database is accessible"""
        if self.calibration:
            self.alarm_timer.stop()
        else:
            # check if the path to the featuredatabase is set and any alarm setting is set
            if any(self.alarm_thresholds.any()):
                if self.trfdbfile:
                    try:
                        # open a constant connection to the trfdatabase
                        if not self.trfdb:
                            self.trfdb = vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro")
                        elif not self.trfdb.connected:
                            self.trfdb = vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro")
                        self.alarm_init = True
                        self.alarm_timer.start(ALARM_CHECK)
                        self.alarm_retrys = 0
                        self.alarm_sqlengine = sa.create_engine(f"sqlite:///{ALARMLOGFILE}")
                    except sqlite3.OperationalError:
                        # may happen if the trfdb is not created (at measurement startup)
                        if self.alarm_retrys < ALARM_MAX_RETRYS:
                            self.message_and_log(f"Going to retry to activate the alarm in {ALARM_REALARM/1000} s.")
                            self.alarm_timer.start(ALARM_REALARM)  # overwrites the ALARM_CHECK interval
                            # [x] TODO add a timer for the re-alarm time
                            self.alarm_retrys += 1
                        else:
                            self.message_and_log(
                                f"Maximal trys ({ALARM_MAX_RETRYS}) to activate the alarm exceeded. Alarm is not active!"
                            )
                            self.alarm_timer.stop()

                else:
                    self.message_and_log("No featuredatabase passed. Can't activate the alarm.")
            else:
                # no thresholds are set -> no alarm possible
                self.message_and_log("No alarm thresholds set. The alarm is deactivated.")
                self.alarm_init = False
                self.alarm_timer.stop()

    def check_alarm(self) -> None:
        """Calculates the alarm score and trigger the alarm
        Initializes the alarm, if not already done.
        """

        if not self.alarm_init:
            self.init_alarm()
            self.alarm_features_checked = False
        elif self.trfdb.connected:
            query = self.get_read_query(self.last_alarm_trai)
            datagenerator = self.trfdb.iread(query_filter=query)
            temp_data = pd.DataFrame(datagenerator)
            if not temp_data.empty:
                cur_data = pd.json_normalize(temp_data.features)
                cur_data = cur_data.set_index(temp_data.trai)
                self.last_alarm_trai = cur_data.index[-1]
                if not self.alarm_features_checked:
                    # only for the replay mode needed
                    self.alarm_features = list(set(self.alarm_features).intersection(cur_data.columns))
                    self.alarm_features_checked = True
                    self.alarm_thresholds.to_sql(
                        name="alarm_thresholds",
                        con=self.alarm_sqlengine,
                        if_exists="append",
                        index=True,
                        index_label="Channel",
                        dtype=sa.types.Numeric,
                    )
                    self.alarm_factors.to_sql(
                        name="alarm_factors",
                        con=self.alarm_sqlengine,
                        if_exists="append",
                        index=False,
                        dtype=sa.types.Numeric,
                    )
                    write_entry = pd.DataFrame({"Score": [self.alarmscore_threshold]})
                    write_entry.to_sql(
                        name="alarm_score",
                        con=self.alarm_sqlengine,
                        if_exists="append",
                        index=False,
                        dtype=sa.types.Numeric,
                    )
                for ch, ch_data in cur_data.groupby("Channel"):
                    alarm_diff = ch_data[self.alarm_features] - self.alarm_thresholds.loc[ch, self.alarm_features]
                    if (alarm_diff > -self.alarmscore_threshold).any().any():

                        self.last_warning[int(ch)] = datetime.now()
                        self.set_channel_warning(int(ch))
                    alarm_diff = alarm_diff.clip(
                        lower=0
                    )  # if current value less than alarm threshold -> clip diff to 0
                    alarm_diff = alarm_diff * self.alarm_factors.loc[ch, self.alarm_features]
                    alarm_diff["Score"] = alarm_diff.sum(axis=1)
                    # [ ] REVIEW here just using if any row, is bigger than score_threshold
                    # also possible after n-times score crossed alarm, ...
                    alarm_result = alarm_diff["Score"] > self.alarmscore_threshold
                    if alarm_result.any():
                        self.last_alarm[
                            int(ch)
                        ] = (
                            datetime.now()
                        )  # [ ] REVIEW writing the timestamp of the triggered alarm not of the timestamp of the corresponding measurement data (delay!)
                        self.set_channel_alarm(int(ch))
                        # [ ] REVIEW logging of the alarm triggers (sometimes lots of entries)
                        write_entry = alarm_diff.loc[
                            alarm_diff["Score"] > self.alarmscore_threshold, "Score"
                        ].to_frame()
                        write_entry["Channel"] = int(ch)
                        if self.replay == "active":
                            write_entry["Mode"] = "Replay"
                        else:
                            write_entry["Mode"] = "Measurement"
                        write_entry["Timestamp"] = pd.to_datetime(self.last_alarm[int(ch)], errors="coerce")
                        write_entry["Featuredb"] = self.outputfile_path.stem

                        write_entry.to_sql(
                            name="alarm_logs",
                            con=self.alarm_sqlengine,
                            if_exists="append",
                            index=True,
                            index_label="TRAI",
                            dtype={
                                "Score": sa.types.Numeric,
                                "Channel": sa.types.Numeric,
                                "Mode": sa.types.Text,
                                "Timestamp": sa.types.DateTime,
                                "TRAI": sa.types.Numeric,
                                "Featuredb": sa.types.Text,
                            },
                        )
                    else:
                        if self.last_alarm[int(ch)]:
                            passed_time = (datetime.now() - self.last_alarm[int(ch)]).total_seconds()
                            if passed_time > ALARM_RESET:
                                self.change_channel_background(int(ch), "green")
                        if self.last_warning[int(ch)]:
                            passed_time = (datetime.now() - self.last_warning[int(ch)]).total_seconds()
                            if passed_time > ALARM_RESET:
                                self.change_channel_background(int(ch), "green")
                                # self.alarm_entry.append(
                                #     [
                                #         [
                                #             abs_time_str,
                                #             record.features["Time"],
                                #             record.features["Channel"],
                                #             feature,
                                #             record.features[feature],
                                #             alarm_threshold,
                                #             record.trai,
                                #         ]
                                #     ]
                                # )
                                # if not self.alarm_entry.empty:
                                #     for ch in self.active_channels:
                                #         if (
                                #             self.alarm_entry.loc[self.alarm_entry["Channel"] == ch, "TRAI"].shape[0]
                                #             >= ALARM_DELAY
                                #         ):
                                #             self.set_channel_alarm(int(record.features["Channel"]))
                                #             if self.first_alarm:
                                #                 self.alarm_logfile_handler.write(
                                #                     self.alarm_entry.iloc[-1], mode="a+", index=False
                                #                 )
                                #             else:
                                #                 self.alarm_logfile_handler.write(
                                #                     self.alarm_entry.iloc[-1], header=False, mode="a+", index=False
                                #                 )
                                #             LOGGER.info(
                                #                 f"Channel {int(record.features['Channel'])} triggered the alarm."
                                #             )

                                # [x] TODO set the Channel to green after time interval again?

    def set_channel_alarm(self, channel: int) -> None:
        self.change_channel_background(channel, "red")

    def set_channel_warning(self, channel: int) -> None:
        self.change_channel_background(channel, "orange")

    def change_channel_background(self, channel: int, color: str) -> None:

        # background/ state of the sensors
        if channel == 1:
            self.ui.label_26.setStyleSheet(f"background-color: {color}")  # Sensor 1
        elif channel == 2:
            self.ui.label_25.setStyleSheet(f"background-color: {color}")  # Sensor 2

    # @qasync.asyncClose
    def closeEvent(self, event):
        super(QMainWindow, self).closeEvent()
        self.message_and_log("Going to close the databases before closing the window.")
        # [ ] TODO the commands below are working, but there are still the -shm and -wal files
        self.stop_plotting()
        if self.tradb:
            self.tradb.close()
            # self.spectrogram_plotter.datagenerator._connection_wrapper.close()
        if self.trfdb:
            self.trfdb.close()
            # for plotter in self.tabs_dynamic_plotters:
            #     if plotter.datagenerator:
            #         plotter.datagenerator._connection_wrapper.close()

        LOGGER.info("Closing Connection to Broker")
        # disconnect the alarm client
        # stop_mqtt(self.client)
        # disconnect all plot clients
        # for plot in self.tabs_dynamic_plotters:
        #     stop_mqtt(plot.client)
        # stop_mqtt(self.spectrogram_plotter.client)
        # await self.session.close()

    def update_progressbar(self) -> None:

        cur_val = self.ui.progressBar.value()
        if cur_val < self.ui.progressBar.maximum():
            self.ui.progressBar.setValue(cur_val + 1)

    # def start_calibration_dialog(self, again=False, dialog: Optional[CalibrationDialog_further] = None) -> None:

    #     if not again:
    #         self.calibration_measurements = []
    #     if dialog:
    #         dialog.close()
    #     self.outputfile_path = None
    #     dlg = CalibrationDialog(
    #         self,
    #         "Kalibrierung",
    #         "Wollen sie eine Kalibrierungmessung auswaehlen oder eine neue Kalibriermessung starten?",
    #     )
    #     dlg.exec()
    #     if not self.calibration:
    #         if self.outputfile_path:
    #             self.calibration_measurements.append(self.outputfile_path)
    #             dlg = CalibrationDialog_further(
    #                 self,
    #                 "Kalibrierung",
    #                 "Wollen sie eine weitere Kalibrierungmessung auswaehlen?",
    #             )
    #             dlg.exec()

    # def automatic_calibration(self, dialog: Optional[CalibrationDialog] = None) -> None:
    #     """Automatic calibration with the default settings"""
    #     if dialog:
    #         dialog.close()
    #     averages = 5
    #     duration = 20
    #     self.do_calibration_measurements(averages, duration)
    #     # waiting to open the file before the measurement time is over
    #     self.ui.progressBar.setMinimum(0)
    #     self.ui.progressBar.setMaximum(averages * duration + 30)  # some tolercane for the startup
    #     self.progressBar_timer.start(1000)
    #     self.ui.progressBar.setValue(0)
    #     self.ui.Process_name.setText("Recording calibration data ...")

    #     QtCore.QTimer.singleShot(
    #         ((averages * duration + 15) * 1000),
    #         lambda: self.evaluate_calibration_measurements(
    #             add_calibration=False, averages=averages, duration=duration
    #         ),
    #     )

    # def do_calibration_measurements(self, averages: int = 5, duration: int = 20, silent=True) -> None:
    #     """Starts the calibration measurements and the automatic evaluation of these measurements

    #     Args:
    #         averages (int, optional): Number of averages. Defaults to 5.
    #         duration (int, optional): Time duration of one average in seconds. Defaults to 20.
    #         silent (bool, optional): True: create automatic an file with the calibration data
    #             False: User has to enter a filename for the config-data
    #     """
    #     # [x] TODO add silent mode (user don't have to set a filelocation)
    #     # [ ] TODO add expert mode (user selectable averages and durations)
    #     self.calibration = (
    #         True  # [ ] Review the calibration flag is deactivated in evaluate_calibration_measurements()
    #     )
    #     if silent:
    #         now = datetime.now()
    #         now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
    #         self.outputfile_path = PurePath(f"data\calibration\{now_str}.tradb")
    #         self.set_filehandler()
    #         self.trfdbfile = PurePath(self.outputfile_path.parent, self.outputfile_path.stem + ".trfdb")
    #         self.alarm_logfile = PurePath(self.outputfile_path.parent, self.outputfile_path.stem + ".csv")
    #         self.alarm_logfile_handler = FileHandler(filename=self.alarm_logfile.name, wkd=self.alarm_logfile.parent)
    #     else:
    #         self.get_file_location(mode="calibration")
    #     calibration_time = averages * duration
    #     self.start_measurement()
    #     self.message_and_log(f"Calibration started. Measurement time: {calibration_time} s. Please wait.")
    #     self.calibration_measurements.append(self.outputfile_path)
    #     # + 15 sec for startup of the measurement
    #     QtCore.QTimer.singleShot((calibration_time + 15) * 1000, self.stop_measurement)

    # def get_laser_record_and_evaluate(self) -> None:

    #     self.get_file_location(mode="open", select_calibration=True)
    #     self.calibration_measurements.append(self.outputfile_path)
    #     self.evaluate_calibration_measurements(add_calibration=False, eval_only=True)

    # def evaluate_calibration_measurements(
    #     self,
    #     add_calibration: bool,
    #     averages: int = 5,
    #     duration: int = 20,
    #     dialog: Optional[CalibrationDialog_further] = None,
    #     eval_only=False,
    # ) -> None:
    #     """Loads the feature data from the database and evaluates the data
    #     The evaluated data is saved in the database.
    #     The evaluation is splitted in a global part and an averaged part, depending to the calibration settings

    #     Args:
    #         add_calibration(bool): True: Add further calibration measurements
    #             False: use the selected calibration mesurement or select one single one
    #         averages (int, optional): Number of averages. Defaults to 5.
    #         duration (int, optional): Time duration of one average in seconds. Defaults to 20."""
    #     if dialog:
    #         dialog.close()
    #     global_max_values = pd.DataFrame(columns=self.alarm_features + ["Channel"])  # create empty pd.DataFrame
    #     if not len(self.calibration_measurements) > 0 or add_calibration:
    #         self.get_file_location(mode="open")
    #         self.calibration_measurements.append(self.outputfile_path)
    #         self.outputfile_path = None
    #         self.f = None
    #         self.trfdbfile = None
    #         self.alarm_logfile = None
    #         self.alarm_logfile_handler = None
    #         # [ ] TODO popup to ask for more calibration files
    #     for file in self.calibration_measurements:
    #         # set here seperatly the filehandler, because the selected files are maybe not at the same location
    #         wkd = file.parent
    #         filename = f"{file.stem}.trfdb"
    #         calibration_f = FileHandler(filename=filename, wkd=wkd)
    #         if calibration_f.exist_file():
    #             with calibration_f.current_file(mode="ro") as trfdb:
    #                 features = trfdb.read()
    #                 # [ ] Review following is not the nicest style
    #                 timestep = features.groupby("Channel")["Time"].agg(lambda x: x.iloc[1] - x.iloc[0]).iloc[0]
    #                 nr_channels = features["Channel"].nunique()
    #                 window_size = int(np.ceil(duration / timestep)) * nr_channels
    #                 features = features[self.alarm_features + ["Channel"]]
    #                 global_stats = features.groupby("Channel").describe()
    #                 # [ ] Review get describe of window_size values, from intervalls with the window_size size, e.g from size 10 intervals
    #                 # -> not perfectly working, there are cases where only 9 values are in the interval, and the last interval is smaller
    #                 # if the size is not a multiple of 10
    #                 interval_stats = features.groupby(["Channel", features.index // window_size]).describe()
    #                 interval_stats_mean = interval_stats.groupby("Channel").mean()
    #                 # [ ] TODO Per sensor and channel show min, max, mean and 75% -> or just set the max or 75% ??
    #                 # [ ] TODO save the complete describe (without count) per sensor and feature
    #                 global_stats = global_stats.unstack(level=0).unstack(level=0).reset_index()
    #                 global_stats = global_stats.rename(columns={"level_0": "Stats"})
    #                 self.save_calibration_stats(
    #                     calibration_f.current_file.path, global_stats, interval_stats, interval_stats_mean
    #                 )
    #                 if not global_max_values.empty:
    #                     global_max_values = (
    #                         pd.concat([global_stats, global_max_values], keys=range(2), names=["DFs"])
    #                         .groupby(["Stats", "Channel"])
    #                         .max()
    #                         .reset_index()
    #                     )
    #                 else:
    #                     global_max_values = global_stats
    #         else:
    #             LOGGER.info(f"Trfdbfile to evaluate the calibration not found: {calibration_f.fullpath}")

    #     threshold_mode = "max"
    #     if not eval_only:
    #         write_thresholds = global_max_values.loc[global_max_values["Stats"] == threshold_mode]
    #         self.write_alarm_settings(write_thresholds)
    #     else:
    #         print_thresholds = global_max_values.loc[global_max_values["Stats"] == threshold_mode]
    #         self.message_and_log("Evaluation results")
    #         for _, row in print_thresholds.iterrows():
    #             # [ ] Make that message and log nicer
    #             self.message_and_log(f"{row}")
    #     self.calibration = False
    #     self.outputfile_path = None
    #     self.trfdbfile = None

    def save_calibration_stats(
        self,
        dbpath: PurePath,
        global_stats: pd.DataFrame,
        interval_stats: pd.DataFrame,
        interval_stats_mean: pd.DataFrame,
    ) -> None:
        """Saves the statistics of a measurement to the corresponding database
        These statistics are used for the calibration (or you get an overview of the features directly in the trfdb)

        Args:
            dbpath (PurePath): database to save the statistics (the feature data is from these db)
            global_stats (pd.DataFrame): global statistics
            interval_stats (pd.DataFrame): statistics of the single intervals
            interval_stats_mean (pd.DataFrame): mean of the statistics of the single intervals
        """

        engine = sa.create_engine(f"sqlite:///{dbpath}")
        insp = sa.inspect(engine)
        tables = list(insp.get_table_names())
        if "trf_stats_global" in tables:
            # if one statistic table is in the database, are there also
            self.message_and_log("There already statistics of the measurement saved!")
            self.message_and_log("Going to overwrite them.")
            # [ ] Review showing the old stats?
        # global stats is "reshaped" earlier
        global_stats.to_sql(name="trf_stats_global", con=engine, if_exists="replace", index=False)
        interval_stats = interval_stats.unstack(level=0).unstack(level=0).unstack(level=0).reset_index()
        interval_stats = interval_stats.rename(columns={"level_0": "Stats", "trai": "Interval"})
        interval_stats.to_sql(name="trf_stats_interval", con=engine, if_exists="replace", index=False)
        interval_stats_mean = interval_stats_mean.unstack(level=0).unstack(level=0).reset_index()
        interval_stats_mean = interval_stats_mean.rename(columns={"level_0": "Stats"})
        interval_stats_mean.to_sql(name="trf_stats_interval_mean", con=engine, if_exists="replace", index=False)

    def load_alarm_settings(self) -> None:
        """Load the current alarm settings from the alarm_settings.yml file and set them active"""
        f = FileHandler(self.alarmsettingsfile_path)
        alarm_settings = f.read()
        calibration_values_d = alarm_settings["Features"]
        self.alarmscore_threshold = alarm_settings["Score"]["threshold"]
        # [ ] REVIEW if there are more than 4 feature in the alarm settings only the first MAX_Features are used
        # [ ] TODO add features only for recording?
        self.alarm_features = list(calibration_values_d.keys())[:MAX_FEATURES]
        # [ ] Review (maybe also review alarm_settings.yml layout)
        temp = pd.DataFrame(calibration_values_d)
        temp = temp.iloc[:, :MAX_FEATURES]
        temp_thresholds = pd.json_normalize(temp.loc["thresholds"]).T
        temp_thresholds.columns = temp.columns
        self.alarm_thresholds = temp_thresholds.loc[temp_thresholds.index.isin(self.active_channels)]
        self.alarm_thresholds.index = self.alarm_thresholds.index.rename("Channel")
        self.alarm_threshols = (
            self.alarm_thresholds.sort_index()
        )  # sort index, if not in ascending order in yml (to prevent iloc logic errors)
        temp_factors = pd.json_normalize(temp.loc["weighting_factors"]).T
        temp_factors.columns = temp.columns
        self.alarm_factors = temp_factors
        self.alarm_factors = temp_factors.loc[temp_factors.index.isin(self.active_channels)]
        self.alarm_factors.index = self.alarm_factors.index.rename("Channel")
        self.alarm_factors = self.alarm_factors.sort_index()
        # [ ] REVIEW the features to record, display, alarm are set in the alarm_settings.yml
        self.features = self.alarm_features
        self.features_units = temp.loc["unit"].to_dict()
        self.display_alarm_thresholds()

    def write_alarm_settings(self, calibration_values: pd.DataFrame = pd.DataFrame()) -> None:
        """Reads the current alarm threshold values from the gui or gets them from the evaluation
        and stores them in the alarm_settings.yml file

        Args:
            calibration_values (pd.DataFrame): calibration values to set"""
        f = FileHandler(self.alarmsettingsfile_path)
        if not calibration_values.empty:
            calibration_values = calibration_values.set_index("Channel")
            calibration_values.index = calibration_values.index.astype(int)
            alarm_thresholds = calibration_values[self.alarm_features]
            self.alarm_thresholds = calibration_values
            self.display_alarm_thresholds()
        else:
            self.get_alarm_thresholds()
            alarm_thresholds = self.alarm_thresholds[self.alarm_features]
        write_d = {"Features": {}, "Score": {"threshold": self.alarmscore_threshold}}
        for feature in self.alarm_features:
            write_d["Features"][feature] = {
                "thresholds": alarm_thresholds.loc[
                    self.alarm_thresholds.index.isin(self.active_channels), feature
                ].to_dict()
            }
            write_d["Features"][feature]["thresholds"].update(
                {key: 0.0 for key in list(set(self.active_channels) - set(self.alarm_thresholds.index.to_list()))}
            )
            write_d["Features"][feature]["weighting_factors"] = self.alarm_factors.loc[
                self.alarm_factors.index.isin(self.active_channels), feature
            ].to_dict()
            # insert 1 for active channels without passed weighting_factor
            write_d["Features"][feature]["weighting_factors"].update(
                {key: 1 for key in list(set(self.active_channels) - set(self.alarm_factors.index.to_list()))}
            )

            write_d["Features"][feature]["unit"] = self.features_units[feature]
        f.current_file.write(content=write_d, mode="w+", comments=ALARMSETTINGS_TIPPS)

    def evaluate_alarm_signal(self, real_alarm: bool) -> None:
        """Evaluate the feature values for a real alarm signal, e.g.: laser fire,
        or a reference signal, which causes similiar acceleration signals than the real alarm signal

        Args:
            real_alarm (bool): True: real alarm signal,
                False: referecne signal
        """
        raise NotImplementedError


def main():
    # def close_future(future, loop):
    #     loop.call_later(10, future.cancel)
    #     future.cancel()

    # loop = asyncio.get_event_loop()
    # future = asyncio.Future()

    app = QApplication(sys.argv)
    # app = qasync.QApplication.instance()

    # if hasattr(app, "aboutToQuit"):
    #     getattr(app, "aboutToQuit").connect(functools.partial(close_future, future, loop))

    mainWindow = MeasurementInterface()
    # await mainWindow.init_mqtt_gui()
    mainWindow.show()

    # await future
    # return True
    sys.exit(app.exec_())


if __name__ == "__main__":
    # source: https://github.com/CabbageDevelopment/qasync/blob/master/examples/aiohttp_fetch.py
    main()
    # try:
    #     qasync.run(main())
    # except asyncio.exceptions.CancelledError:
    #     sys.exit(0)
