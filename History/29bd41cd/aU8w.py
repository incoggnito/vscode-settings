import asyncio
import os
import sys
from datetime import datetime
from functools import partial
from io import StringIO
from pathlib import Path, PurePath
from typing import Dict

import quamash

# from quamash import QEventLoop
from asyncqt import QEventLoop, asyncSlot
from atoolbox import JsonFile
from vallendb import PridbFile
from PyQt5.QtCore import QLine, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QTextLine
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

from fyrsonic.measurement.configuration import create_config
from fyrsonic.opcua_servers.conditionWave import start_measurement
from fyrsonic.utils.input_handler import select_list_entry

FIGURES = PurePath(Path(__file__).resolve().parent, "figures")


class BasicGui(QWidget):
    def __init__(self, labels: Dict, pridbfile: PridbFile, loop=None):
        super().__init__()
        self.loop = loop if not None else asyncio.get_event_loop()
        self.buildGUI(labels, pridbfile)

    def buildGUI(self, labels: Dict, pridbfile: PridbFile) -> None:

        sys.stdout = EmittingStream(textWritten=self.pass_prints_out)
        sys.stderr = EmittingStream(textWritten=self.pass_prints_out)

        self.setGeometry(300, 300, 450, 350)
        self.setWindowTitle("Measurement Interface")

        self.startbutton = QPushButton("Start Measurement", self)
        self.startbutton.clicked.connect(self.measurement_wrapper)

        self.stopbutton = QPushButton("Stop", self)
        self.stopbutton.clicked.connect(self.stopGUI)

        self.cmd_0 = QLabel(self)
        self.cmd_0.setText("Ready for user input!")
        self.cmd_1 = QLabel(self)
        self.cmd_1.setText("Ready for user input!")
        self.cmd_2 = QLabel(self)
        self.cmd_2.setText("Ready for user input!")
        self.cmd_3 = QLabel(self)
        self.cmd_3.setText("Ready for user input!")
        self.cmd_4 = QLabel(self)
        self.cmd_4.setText("Ready for user input!")
        self.cmd_5 = QLineEdit(self)
        self.cmd_5.returnPressed.connect(self.handle_user_input)

        # sys.stdin = IncomingStream(self.handle_user_input())
        # sys.stdin = self.handle_user_input()
        # self.re.move(130, 22)

        # self.le = QLineEdit(self)
        # self.le.move(200, 22)
        self.logo = QLabel(self)
        self.textline = QLabel(self)
        self.textline.setText("No label so far.")
        pixmap = QPixmap(str(PurePath(FIGURES, "LogoAMITRONICS.png")))
        self.logo.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.create_label_buttons(labels, pridbfile)
        self.new_label = QLineEdit(self)
        self.new_label_button = QPushButton("Add new label:", self)
        self.new_label_button.clicked.connect(
            partial(self.handle_button_input, self.new_label.text(), pridbfile)
        )

        self.grid = QGridLayout(self)
        self.grid.addWidget(self.startbutton, 1, 1)
        self.grid.addWidget(self.cmd_0, 2, 1)
        self.grid.addWidget(self.cmd_1, 3, 1)
        self.grid.addWidget(self.cmd_2, 4, 1)
        self.grid.addWidget(self.cmd_3, 5, 1)
        self.grid.addWidget(self.cmd_4, 6, 1)
        self.grid.addWidget(self.cmd_5, 7, 1)
        self.grid.addWidget(self.logo, 1, 5)
        self.grid.addWidget(self.new_label, 4, 11)
        self.grid.addWidget(self.new_label_button, 4, 10)
        self.arrange_buttons(labels)
        self.grid.addWidget(self.textline, 1, 12)
        self.setLayout(self.grid)
        self.show()

    # def showDialog(self):
    #     text, ok = QInputDialog.getText(self, "Label measurement", "Enter label:")

    #     if ok:
    #         timestamp = datetime.now()
    #         self.le.setText(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
    #         self.re.setText(str(text))
    @asyncSlot()
    async def measurement_wrapper(self) -> None:

        await start_measurement()

    def handle_button_input(self, buttonname: str, pridbfile: PridbFile):

        # TODO add writing in pridb
        timestamp = datetime.now()
        time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        pridbfile.write_label(buttonname, timestamp)
        self.textline.setText(f"{time_str} {buttonname}")

    def create_label_buttons(self, labels: Dict, pridbfile: PridbFile) -> None:
        """Creates QPushButtons for all labels

        Args:
            labels (Dict): Labels (with Position as values), only the keys are used here
        """
        buttons = []

        for i, label in enumerate(labels.keys()):
            buttons.append(QPushButton(label, self))
            buttons[i].clicked.connect(
                partial(self.handle_button_input, label, pridbfile)
            )
        self.buttons = buttons

    def arrange_buttons(self, labels: Dict) -> None:
        """Arrange the buttons with the labes at the specified positions (values in the dict)

        Args:
            labels (Dict): Labels (with Position as values)
        """

        for i, position in enumerate(labels.values()):
            self.grid.addWidget(self.buttons[i], *position)

    def pass_prints_out(self, text: str) -> None:

        self.cmd_0.setText(self.cmd_1.text())
        self.cmd_1.setText(self.cmd_2.text())
        self.cmd_2.setText(self.cmd_3.text())
        self.cmd_3.setText(self.cmd_4.text())
        self.cmd_4.setText(text)

    def handle_user_input(self) -> None:

        # with StringIO(f"{self.cmd_5.text()}\n") as text:
        #     sys.stdin = text

        sys.stdin = StringIO(f"{self.cmd_5.text()}\n")
        self.cmd_4.setText(f"{self.cmd_5.text()}")
        # self.textline.setText(self.cmd_5.text())

    def stopGUI(self) -> None:

        print("Saving...")
        print("Closing...")
        self.close()

    def __del__(self) -> None:
        # Restore sys.stdout
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        sys.stdin = sys.__stdin__
        self.loop.close()


class EmittingStream(QObject):

    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


# class IncomingStream(QObject):

#     textInput = pyqtSignal(str)

#     def readline(self, StringIO) -> str:
#         self.textInput.emit(StringIO)


def run_gui(labels: Dict, pridbfile: PridbFile) -> None:
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    with loop:
        ex = BasicGui(labels, pridbfile, loop)
        ex.show()
        loop.run_forever()
    sys.exit(app.exec_())


if __name__ == "__main__":

    DATA = PurePath(Path(__file__).resolve().parents[3], "data")
    label_path = PurePath(DATA, "Settings\\GUI\\Label_options.json")
    labelfile = JsonFile(file_obj=label_path)
    labels = labelfile.read()
    MEASUREMENTS = PurePath(DATA, "Measurements")
    if not os.path.exists(MEASUREMENTS):
        os.makedirs(MEASUREMENTS)

    options = [
        "Manually input the measurement settings",
        "Use the measurement settings file?",
    ]
    inp = asyncio.run(select_list_entry("Measurement settings:", options))
    cW_options = PurePath(DATA, "Settings\\measurement\\ConditionWave_options.json")
    if inp == options[0]:
        config = asyncio.run(create_config(cW_options))
    else:
        settings = PurePath(DATA, "Settings\\measurement\\ConditionWave_settings.json")
        config = asyncio.run(create_config(cW_options, settings))
    pridb_path = PurePath(MEASUREMENTS, "Test.pridb")
    pridbfile = PridbFile(pridb_path, config["Datastream 1"], "rwc")

    run_gui(labels, pridbfile)
    pridbfile.close()
