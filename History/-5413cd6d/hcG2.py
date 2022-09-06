from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QMainWindow,
    QVBoxLayout,
)

from PySide2 import QtCore
import sys
from pathlib import Path, PurePath
import pandas as pd
import numpy as np
import os
from typing import Optional
import vallenae as vae
from fyrsonic.measurement.measurement_interface import start_measurement
from fyrsonic.measurement import trfdb_writer
import logging
import os
import signal
import sqlite3
import sys
import inspect


import time
from datetime import datetime
from pathlib import Path, PurePath
from typing import Optional
import numpy as np

import pandas as pd
import vallenae as vae
from atoolbox import FileHandler
from bigtoolbox.BigFileHandler.utils import read_acq_settings
from fyrsonic.measurement import measurement_interface, trfdb_writer

from ui_files.CMS_GUI import Ui_MainWindow

# [ ] TODO get the logo and the Icon working again
# [ ] TODO visualize active state with colored label
# [ ] TODO add a check which devices (conditionWave, TiePies) are connected -> user choice which one to use
# [ ] TODO config files for every device seperatly

formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# LOGGER_IMPORTED_MODULES = logging.getLogger("asammdf")  # [ ] TODO not working
# LOGGER_IMPORTED_MODULES.setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)
today = datetime.today()
today_str = today.strftime("%Y_%m_%d")
LOGFILE = Path(r"data\logs", today_str + ".log").absolute()
handler = logging.FileHandler(LOGFILE, mode="a+")
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
# consoleHandler.setLebel(logging.DEBUG)
LOGGER.addHandler(consoleHandler)
LOGGER.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.INFO)

# [ ] TODO get the lowpass filter working

# [ ] TODO better to use the filehandler here?
PYTHON_VENV = str(Path(r"venv\Scripts\python.exe").absolute())
CONFIGFILE_PATH = PurePath(r"data/settings/measurement_settings.json")
ALARMSETTINGSFILE_PATH = PurePath(r"data/settings/alarm_settings.yml")
DISPLAY_INTERVAL = 100  # ms
READ_BLOCKS = 100  # max. number of blocks to read at once (for plotting)
# arbitrary values just for init, could be maybe higher
MAX_SAMPLEFREQUENCY = 1_000_000
MAX_BLOCKSIZE = 2 ** 18
MAX_CHANNELS = 2
# REVIEW read by time instead by blocks

OVERLAP = 0.5
ALARM_CHECK = 2  # ms
ALARM_DELAY = 10  # number of blocks
# corresponding delay time: ALARM_DELAY * blocksize/samplefrequency

# [ ] TODO not saving data (tempfile which is going to be deleted) or writing to stream/buffer?
# [ ] TODO rename the tabs and other element to increae the possiblity to understand which element is meant in the python code

# [ ] TODO if starting a further measurement only the tradb is started but not the feature saving

# [ ] TODO store the timestamps of alarms (include which channel and features with treshold and actual level)
# [x] TODO add a button to reset the alarm
# [ ] TODO don't forget to set correct range (get the range with the mulichannel software -> edit config file)


class FileDialog(QDialog):
    def __init__(self, parent: QMainWindow, windowtitle: str, message: str, mode="save"):
        # [ ] Review variable type is not that specific, but MainWindow is declared later and it is not possible to declare SaveDialog later
        super().__init__()

        self.setWindowTitle(windowtitle)
        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No
        self.buttonBox = QDialogButtonBox(QBtn)
        # lambda function is needed to pass the SaveDialog object to close it in get_file_location
        self.buttonBox.accepted.connect(lambda: parent.get_file_location(self, mode=mode))
        self.buttonBox.rejected.connect(self.close)  # do nothing if no is clicked

        self.layout = QVBoxLayout()
        message = QLabel(message)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
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
        self.first_alarm = True
        self.tradb = None
        self.last_plot_trai = 1
        self.last_alarm_trai = 1
        self.display_interval = DISPLAY_INTERVAL

        # QTimer
        self.alarm_timer = QtCore.QTimer()
        self.alarm_timer.timeout.connect(self.check_alarm)

        self.active_channels = []

        self.features = [
            "Hit_Peak",
            "RMS",
            "Crest_Factor",
            "HFC",
        ]  # ["Amplitude", "RMS", "Energy", "HFC"]  # ["Crest_Factor", "RMS", "HFC", "K_Factor"]
        self.features_units = ["V", "V", "", "V**2/Hz"]
        self.alarm_features = (
            self.features
        )  # [ ] REVIEW skipp that safty save # going to drop later the features not in the trfdb for the alarm triggering
        # alarm_factors currently set to 1 for all features
        self.alarm_factors = pd.DataFrame([len(self.alarm_features) * [1]], columns=self.alarm_features)

        # rename the feature tabs
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_2), self.features[0])
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_5), self.features[1])
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_6), self.features[2])
        self.ui.tabWidget.setTabText(self.ui.tabWidget.indexOf(self.ui.tab_7), self.features[3])

        self.p_meas = None
        # [ ] TODO enable pridbwriting, if measuring with the fyrsonic (Visual AE desiered)
        # self.p_pridb = None
        self.p_trfdb = None
        self.replay = "no"

        self.tabs_dynamic_plotters = []

        # [ ] TODO units of the DynamicFeaturePlotter!
        # tab 2: Amplitude plot
        self.ui.graphicsView.init_plot(
            self.features[0],
            self.features[0],
            unit=self.features_units[0],
            display_interval=DISPLAY_INTERVAL,
            read_blocks=READ_BLOCKS,
        )
        self.tabs_dynamic_plotters.append(self.ui.graphicsView)

        # tab 3: RMS plot
        self.ui.graphicsView_2.init_plot(
            self.features[1],
            self.features[1],
            unit=self.features_units[1],
            display_interval=DISPLAY_INTERVAL,
            read_blocks=READ_BLOCKS,
        )
        self.tabs_dynamic_plotters.append(self.ui.graphicsView_2)

        # tab 4: HFC plot
        self.ui.graphicsView_3.init_plot(
            self.features[2],
            self.features[2],
            unit=self.features_units[2],
            display_interval=DISPLAY_INTERVAL,
            read_blocks=READ_BLOCKS,
        )
        self.tabs_dynamic_plotters.append(self.ui.graphicsView_3)

        # tab 5: Energy plot
        self.ui.graphicsView_4.init_plot(
            self.features[3],
            self.features[3],
            unit=self.features_units[3],
            display_interval=DISPLAY_INTERVAL,
            read_blocks=READ_BLOCKS,
        )
        self.tabs_dynamic_plotters.append(self.ui.graphicsView_4)

        # tab 6: spectrogram
        self.ui.graphicsView_5.init_plotwindow(
            display_interval=50,
            read_blocks=READ_BLOCKS,
        )
        self.spectrogram_plotter = self.ui.graphicsView_5

        self.ui.comboBox_2.currentIndexChanged.connect(self.plot_spectrogram)

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
        self.ui.pushButton_6.pressed.connect(self.reset_alarm_state)

        # background/ state of the sensors
        self.reset_alarm_state()

        self.display_current_settings()

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
        self.get_settings()
        if not self.outputfile_path:
            dlg = FileDialog(
                self,
                "Speichern ?",
                "Sollen die Messdaten gespeichert werden?",
                mode="save",
            )
            dlg.exec()

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
            self.start_trfdb_writer()
        else:
            self.message_and_log("Measurement script is running please wait.")

        # self.timer.start(self.display_interval)

    def stop_measurement(self):
        if self.p_meas:
            if self.p_meas.state() == QtCore.QProcess.Running:
                self.message_and_log("Stopping measurement.")
                pid = self.p_meas.processId()
                if os.name == "nt":  # windows machine
                    for _ in range(5):
                        try:
                            os.kill(pid, signal.CTRL_C_EVENT)  # CTRL-C on windows machines
                            time.sleep(0.75)
                        except PermissionError:
                            continue
                        except KeyboardInterrupt:
                            # not sure why the KeyboardInterrupt is recogniced here (should only send to the measurement script)
                            continue
                else:
                    for _ in range(5):
                        try:
                            os.kill(pid, signal.SIGINT)  # SIGINT is CTRL-C (linux machines)
                            time.sleep(0.75)
                        except PermissionError:
                            continue
                stop = datetime.now()
                stop_str = stop.strftime("%Y_%m_%d_%H_%M_%S.%f")
                LOGGER.debug(f"Last tradb stop signal send at: {stop_str}")
                self.p_meas.waitForFinished(5000)
                self.p_meas.finished.connect(lambda: self.message_and_log("Measurement process finished."))
            # self.p_meas = None
            # self.p_pridb.waitForFinished(5000)
            # self.p_pridb = None
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
            self.p_trfdb.start(
                str(PYTHON_VENV),
                [
                    str(trfdb_writer_script),
                    "-i " + str(self.outputfile_path),
                    "-f " + (", ").join(self.features),
                ],
            )
            self.trfdbfile = PurePath(self.outputfile_path.parent, self.outputfile_path.stem + ".trfdb")
            self.alarm_timer.start(ALARM_CHECK)
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
        elif tabIndex == 6:
            # channel = self.ui.comboBox.currentIndex() + 1
            # sensor inspection tab
            self.plot_timedata(0)
            for i in range(4):
                self.tabs_dynamic_plotters[i].stop_update_routine()
            # if self.trfdb:
            #     self.trfdb.close()
            self.spectrogram_plotter.stop_update_routine()

    def plot_featuredata(self, index: int) -> None:
        if not self.replay in ["pause", "stopp"]:
            if self.trfdbfile:
                if not self.trfdb:
                    self.trfdb = vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro")
                elif not self.trfdb.connected:
                    self.trfdb = vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro")
                    # [ ] Review using last plot trai for all plots
                datagenerator = self.trfdb.iread(
                    query_filter=f"trai >= {self.last_plot_trai} AND trai < {self.last_plot_trai+READ_BLOCKS}"
                )
                self.tabs_dynamic_plotters[index - 1].start_update_routine(datagenerator, self.active_channels)
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
                    # [ ] Review using last plot trai for all plots
                datagenerator = self.tradb.iread(
                    query_filter=f"trai >= {self.last_plot_trai} AND trai < {self.last_plot_trai+READ_BLOCKS}"
                )
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
                # [ ] Review using last plot trai for all plots
                datagenerator = self.tradb.iread(
                    query_filter=f"trai >= {self.last_plot_trai} AND trai < {self.last_plot_trai + READ_BLOCKS}"
                )
                channel = self.ui.comboBox_2.currentIndex() + 1
                self.spectrogram_plotter.start_update_routine(datagenerator, channel, overlap=OVERLAP)
            else:
                self.message_and_log("Can't plot anything without an transient database.")

    def handle_stderr(self, process: QtCore.QProcess):
        # logging prints to stderr per default
        data = process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self, process: QtCore.QProcess):
        data = process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def handle_state(self, state, process_name: str):
        # [ ] TODO maybe add a constant light of the process state
        states = {
            QtCore.QProcess.NotRunning: "Not running",
            QtCore.QProcess.Starting: "Starting",
            QtCore.QProcess.Running: "Running",
        }
        state_name = states[state]
        self.message_and_log(f"{process_name} State changed: {state_name}")

    def get_file_location(self, filedialog: Optional[FileDialog] = None, mode: str = "save", attempt: int = 0) -> None:

        if filedialog:
            filedialog.close()
        if mode == "save":
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
            self.alarm_logfile = PurePath(self.outputfile_path.parent, self.outputfile_path.stem + ".csv")
            self.alarm_logfile_handler = FileHandler(filename=self.alarm_logfile.name, wkd=self.alarm_logfile.parent)
        else:
            attempt += 1
            if attempt < 4:
                self.get_file_location(filedialog, mode, attempt)
            else:
                self.message_and_log("4 attemps to set the featuredatabase for saving failed.")
                # [ ] TODO break here?

    def set_filehandler(self) -> None:
        if self.outputfile_path:
            wkd = self.outputfile_path.parent
            filename = f"{self.outputfile_path.stem}.tradb"
            self.f = FileHandler(filename=filename, wkd=wkd)
            self.outputfile_path = self.f.current_file.path
        if self.f.exist_file() and self.replay == "no":
            now = datetime.now()
            now_str = now.strftime("%Y_%m_%d_%H_%M_%S")
            wkd = self.outputfile_path.parent
            filename = f"{self.outputfile_path.stem}_{now_str}.tradb"
            self.f = FileHandler(filename=filename, wkd=wkd)
            self.outputfile_path = self.f.current_file.path
            # self.tradb_exist = True

    def get_settings(self) -> None:
        self.get_activated_channels()
        self.get_alarm_thresholds()
        self.get_filter_settings()

    def set_settings(self) -> None:
        # [ ] TODO set all settings not editable during measurement?
        self.get_settings()
        self.write_settings_to_configfile()

    def get_activated_channels(self) -> None:

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
                self.trfdb = vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro")
            except sqlite3.OperationalError:
                self.message_and_log("Can not connect to the feature database. Replay mode not possible.")
                self.message_and_log("Please check the path to the feature database.")
            # reading of only the MAX channels would be sufficent
            records = self.trfdb.read(query_filter=f"trai >= 1 AND trai <= {2*MAX_CHANNELS}")
            self.active_channels = records["Channel"].unique().tolist()

    def get_alarm_thresholds(self) -> None:

        # checkout the ui file with qt-designer to get the elment names
        # [ ] Rename the elements with qt-designer to get the needed names straightforward
        # [x] TODO implement that flexible
        self.alarm_thresholds = pd.DataFrame()
        # first feature (amplitude)
        self.alarm_thresholds[self.alarm_features[0]] = pd.Series(
            [
                self.ui.doubleSpinBox.value(),
                self.ui.doubleSpinBox_2.value(),
            ]
        )
        # second feature (RMS)
        self.alarm_thresholds[self.alarm_features[1]] = pd.Series(
            [
                self.ui.doubleSpinBox_7.value(),
                self.ui.doubleSpinBox_8.value(),
            ]
        )

        # third feature (Hochfrequenter Anteil)
        self.alarm_thresholds[self.alarm_features[2]] = pd.Series(
            [
                self.ui.doubleSpinBox_13.value(),
                self.ui.doubleSpinBox_14.value(),
            ]
        )

        # 4th feature (Energie)
        self.alarm_thresholds[self.alarm_features[3]] = pd.Series(
            [
                self.ui.doubleSpinBox_19.value(),
                self.ui.doubleSpinBox_20.value(),
            ]
        )
        self.alarm_thresholds.index = np.arange(1, self.alarm_thresholds.shape[0] + 1)

    def get_filter_settings(self) -> None:

        # checkout the ui file with qt-designer to get the elment names
        # lower cut-off frequency
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

    def display_current_settings(self) -> None:
        # [x] TODO display the current settings from the config file
        # [ ] TODO add read and save of the alarm configs!
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
        for i, row in settings_df.iterrows():
            if i > 0:  # skip first row
                low_filter = 0
                if row["Lowpass Filter Cutoff Frequency"]:  # None values are possible -> set them to 0
                    temp = float(row["Lowpass Filter Cutoff Frequency"])
                    if not np.isnan(temp):
                        low_filter = int(temp)
                high_filter = 0
                if row["Highpass Filter Cutoff Frequency"]:  # None values are possible -> set them to 0
                    temp = float(row["Highpass Filter Cutoff Frequency"])
                    if not np.isnan(temp):
                        high_filter = int(temp)
                if row.Channel == 1:
                    self.ui.spinBox.setValue(low_filter)
                    self.ui.spinBox_7.setValue(high_filter)
                elif row.Channel == 2:
                    self.ui.spinBox_2.setValue(low_filter)
                    self.ui.spinBox_8.setValue(high_filter)
        if not settings_df.loc[1:, "Additional Text"].isna().all():
            # [ ] TODO select all not None/nan/Null text
            # add_text = settings_df.loc[settings_df.loc[1:, "Additional Text"].isna(), "Additional Text"]
            self.ui.lineEdit_13.setText((" ").join(settings_df.loc[1:, "Additional Text"].astype(str)).strip())

    def replay_measurement(self) -> None:
        # [ ] TODO get the state if the measurement is over -> new init the replay
        if not self.replay == "pause":
            self.replay = "active"  # is checked in get_file_location
            self.get_file_location(None, mode="open")
            if self.outputfile_path:
                self.get_activated_channels()
                self.display_current_settings()
                self.get_alarm_thresholds()
                self.restart_plotting()
                self.reset_alarm_state()
            else:
                self.replay == "no"
        else:
            self.replay = "active"

        self.alarm_timer.start(ALARM_CHECK)

    def pause_replay(self) -> None:
        self.replay = "pause"
        self.alarm_timer.stop()
        self.stop_plotting()

    def stop_replay(self) -> None:
        self.replay = "stopp"
        self.outputfile_path = None
        self.alarm_timer.stop()
        self.stop_plotting()
        self.restart_plotting()

    def restart_plotting(self) -> None:
        self.last_alarm_trai = 1
        self.last_plot_trai = 1
        for i in self.tabs_dynamic_plotters:
            i.last_trai = 1
            i.channels_checked = False
            i.plot_init = False
        self.spectrogram_plotter.last_trai = 1

    def stop_plotting(self) -> None:
        for plotter in self.tabs_dynamic_plotters:
            plotter.stop_update_routine()
        self.spectrogram_plotter.stop_update_routine()

    def reset_alarm_state(self) -> None:

        for ch in range(1, 7):
            self.change_channel_background(ch, "green")

    def check_alarm(self) -> None:

        # check if any alarm setting is set
        if self.trfdbfile and any(self.alarm_thresholds.any()):
            successfull = True
            try:
                if not self.trfdb:
                    self.trfdb = vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro")
                elif not self.trfdb.connected:
                    self.trfdb = vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro")
            except sqlite3.OperationalError:
                # may happen if the trfdb is not created (at measurement startup)
                time.sleep(2)
                try:
                    self.trfdb = vae.io.TrfDatabase(filename=self.trfdbfile, mode="ro")
                except:
                    self.message_and_log("Can not connect to the feature database. Going to deactivate the alarm!")
                    self.alarm_timer.stop()
                    # [ ] TODO add a timer for the re-alarm time
                    successfull = False
            if successfull:
                datagenerator = self.trfdb.iread(
                    query_filter=f"trai >= {self.last_alarm_trai} AND trai < {self.last_alarm_trai+READ_BLOCKS}"
                )
                temp_data = pd.DataFrame(datagenerator)
                if not temp_data.empty:
                    cur_data = pd.json_normalize(temp_data.features)
                    if not self.alarm_features_checked:
                        self.alarm_features = list(set(self.alarm_features).intersection(cur_data.columns))
                    for ch, ch_data in cur_data.groupby("Channel"):
                        alarm_diff = ch_data[self.features] - self.alarm_thresholds.loc[ch, self.features]
                        alarm_diff = alarm_diff.clip(
                            lower=0
                        )  # if current value less than alarm threshold -> clip diff to 0
                        alarm_diff = alarm_diff * self.alarm_factors[self.features]
                for record in datagenerator:
                    for feature in record.features.keys():
                        if feature in self.alarm_thresholds.columns:
                            channel = int(record.features["Channel"])
                            alarm_threshold = self.alarm_thresholds.loc[channel, feature]
                            # TODO use a combined score with multiple features
                            if record.features[feature] > alarm_threshold and alarm_threshold > 0.0:
                                if self.replay == "no":
                                    now = datetime.now()
                                    abs_time_str = now.strftime("%Y_%m_%d_%H_%M_%S")
                                else:
                                    abs_time_str = "Replay mode"
                                self.set_channel_alarm(int(record.features["Channel"]))
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

                                # [ ] TODO set the Channel to green after time interval again?

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

    def closeEvent(self, *args, **kwargs):
        super(QMainWindow, self).closeEvent(*args, **kwargs)
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


def main():
    app = QApplication(sys.argv)
    w = MeasurementInterface()
    w.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
