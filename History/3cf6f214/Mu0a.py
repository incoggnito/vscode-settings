import collections
import numpy as np
import pyqtgraph as pg
import pandas as pd
from PySide2 import QtCore
from typing import List, Tuple, Optional, Dict
import logging
from vaspy.process import rolling_average
from measurementgui.utils.mqtt.mqtt_standard import init_mqtt

formatter = logging.Formatter(fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
LOGGER = logging.getLogger(__name__)

# global parameters for databuffering
MAX_CHANNELS = 2
# currently the measurement devices only support max. 6 channels at once
MAX_PLOT_POINTS = 100000 * MAX_CHANNELS
COLORS = ["b", "g", "r", "c", "m", "k"]


class DynamicFeaturePlotter(pg.GraphicsLayoutWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.plt = None

    def init_plot(
        self,
        source_column: str,
        ylabel: str,
        unit: str = "V",
        display_interval: int = 250,  # milliseconds
        read_blocks: Optional[int] = None,  # max. blocks to read at once
        plot_blocks: int = 1000,
        smooth_data: bool = False,
        mqtt_config: Optional[Dict] = None,
        size=(600, 350),
    ):
        # possible colors: https://pyqtgraph.readthedocs.io/en/latest/style.html
        # (b, g, r, c, m, y, k, w)
        self.display_interval = display_interval
        # Data stuff
        self.last_trai = 1
        self.read_blocks = read_blocks
        self.plot_blocks = plot_blocks
        self.smooth_data = smooth_data
        if self.plot_blocks > MAX_PLOT_POINTS:
            self.bufsize = MAX_PLOT_POINTS
        else:
            self.bufsize = self.plot_blocks
        self.source_column = source_column
        self.x = np.linspace(-10, 0.0, self.bufsize)  # -10s just for init
        self.y = np.zeros((MAX_CHANNELS, self.bufsize), dtype=float)
        self.timevector_updated = False
        self.datagenerator = None
        self.channels_checked = False
        self.client = None
        self.mqtt_config = mqtt_config
        self.channels = list(range(1, MAX_CHANNELS + 1))

        # PyQtGraph stuff
        if self.plt:
            self.removeItem(self.plt)
        self.plt = self.addPlot()  # pg.PlotWidget()
        # self.plt.setTitle("Amplitude [V]")
        # self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        # self.plt.setXRange(5,20, padding=0)
        fontcolor = "#000000"
        labelStyle = {"color": fontcolor}
        self.plt.setLabel("left", ylabel, unit, **labelStyle)
        self.plt.setLabel("bottom", "Zeit", "s", **labelStyle)
        self.plt.axes["bottom"]["item"].style["showValues"] = False
        self.setBackground("w")
        self.plt.addLegend()
        self.curve = []
        self.databuffers = []
        for i in range(1, MAX_CHANNELS + 1):
            self.databuffers.append(collections.deque([0.0] * self.bufsize, self.bufsize))
            if self.smooth_data:
                curve = self.plt.plot(
                    self.x,
                    rolling_average(self.y[i - 1, :], 50),
                    pen=pg.mkPen(color=COLORS[i - 1]),
                    name=f"Sensor {i}",
                )
            curve = self.plt.plot(
                self.x,
                self.y[i - 1, :],
                pen=pg.mkPen(color=COLORS[i - 1]),
                name=f"Sensor {i}",  # if updating this name, the changes must be considered in the check_channels() !
            )
            self.curve.append(curve)
            # )  # , width=2)
            # )
            # )
        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.update = True
        if self.mqtt_config:
            self.client = init_mqtt(
                mqtt_config,
                mqtt_topics=["vam_data"],
                client_name="MeasurementGUI_plot_subscriber",
                on_message_func=[self.updateplot],
            )

    def start_update_routine(self, datagenerator, active_channels: List[int]) -> None:
        self.update = True
        self.channels = active_channels
        self.datagenerator = datagenerator
        self.channels_checked = False
        self.timer.start(self.display_interval)

    def stop_update_routine(self) -> None:
        self.timer.stop()
        if self.client:
            self.client.disconnect()
        self.update = False

    def reset_plot(self) -> None:
        self.datagenerator = None
        self.last_trai = 1
        self.channels_checked = False
        self.plot_init = False

    def getdata(self) -> pd.DataFrame:

        records_temp = pd.DataFrame(self.datagenerator)
        if not records_temp.empty:
            records = pd.json_normalize(records_temp.features)
            records = records.set_index(records_temp.trai)
            self.last_trai = records.index[-1]
            # [ ] Review modifying the sql-query of the existing generator
            # [ ] TODO check if always working
            query = self.datagenerator._query.splitlines()
            if self.read_blocks:
                query[-1] = f" WHERE (trai > {self.last_trai}) AND (trai < {self.last_trai + self.read_blocks})"
            else:
                query[-1] = f" WHERE trai > {self.last_trai}"
            query = ("\n").join(query)
            self.datagenerator._query = query
        else:
            records = pd.DataFrame()

        if not self.update:
            records = pd.DataFrame()

        return records

    def check_channels(self, relevant_data: pd.DataFrame) -> None:

        # there are no channels selected, plotting all channels in db
        # this can only happen in replay mode
        channels_in_db = relevant_data.Channel.unique()
        if not len(self.channels) > 0:
            self.channels = channels_in_db
            # [ ] REVIEW Design Decision -> replay mode only show max channels of the connected device or show all channel data in the db?
            self.channels = self.channels[:MAX_CHANNELS]
        else:
            # remove activated channels, which are not in the db
            self.channels = list(set(self.channels) & set(channels_in_db))
            # [ ] REVIEW Design Decision -> replay mode only show max channels of the connected device or show all channel data in the db?
            self.channels = self.channels[:MAX_CHANNELS]
        for curve in self.curve:
            # [ ] Review that maybe very errorproune: only working for max. 99 Sensors and automatic legend should not be updated!
            if not int(curve.name()[-2::]) in channels_in_db:
                self.plt.removeItem(curve)
        self.channels_checked = True

    def updateplot(self, plot_data: Optional[pd.DataFrame] = None):
        if not plot_data:
            relevant_data = self.getdata()
        else:
            relevant_data = pd.DataFrame([plot_data])
        if not relevant_data.empty:
            # updates = 20
            # [ ] TODO get channel check working for mqtt data
            if not self.channels_checked and not self.client:
                self.check_channels(relevant_data)
            if self.source_column in relevant_data.columns:
                for ch in self.channels:
                    ch = int(ch)  # ch can be a float
                    # for element in relevant_data:
                    data = relevant_data.loc[relevant_data["Channel"] == ch, self.source_column]
                    if not self.timevector_updated and relevant_data.shape[0] > 1:
                        timepoints = relevant_data.loc[relevant_data["Channel"] == ch, "Time"]
                        timestep = timepoints.iloc[0] - timepoints.iloc[1]
                        timestart = self.bufsize * timestep
                        # [ ] Review that x_vector maybe don't use x-ticks, there may be latency and the time ticks may be not correct?
                        self.x = np.linspace(timestart, 0.0, self.bufsize)
                        self.plt.setXRange(self.x.min(), self.x.max())
                        self.timevector_updated = True
                    new_plot_data = data.iloc[-self.bufsize :].to_numpy()
                    # [ ] Review not possible to append list at once -> better to use list instead of deque?
                    for el in new_plot_data:
                        self.databuffers[ch - 1].append(el)
                    self.y[ch - 1, :] = np.array(self.databuffers[ch - 1])
                    if self.smooth_data:
                        self.curve[ch - 1].setData(self.x, rolling_average(self.y[ch - 1, :], 50))
                    else:
                        self.curve[ch - 1].setData(self.x, self.y[ch - 1, :])
            else:
                LOGGER.warning("This feature is not in the feature database.")
                self.update = False
                self.timer.stop()

        else:
            LOGGER.debug(f"Data is over: {self.last_trai}")


class DynamicTimePlotter(pg.GraphicsLayoutWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.plt = None

    def init_plot(
        self,
        color: str = "b",  # "b",  # "g", "r", "c", "m", "k"
        unit: str = "V",
        display_interval: int = 250,  # milliseconds
        read_blocks: Optional[int] = None,  # max. blocks to read at once
        size=(600, 350),
        mqtt_config: Optional[Dict] = None,
    ):
        # possible colors: https://pyqtgraph.readthedocs.io/en/latest/style.html
        # (b, g, r, c, m, y, k, w)
        self.display_interval = display_interval
        self.read_blocks = read_blocks
        self.color = color
        # Data stuff
        self.last_trai = 1
        self.bufsize = MAX_PLOT_POINTS
        self.nr_blocks = 0
        self.x = np.linspace(-10, 0.0, self.bufsize)  # -10 s just for init
        self.y = np.zeros(self.bufsize, dtype=float)
        self.databuffer = collections.deque([0.0] * self.x.size, self.x.size)
        self.timevector_updated = False
        self.datagenerator = None
        self.client = None
        self.mqtt_config = mqtt_config

        # PyQtGraph stuff
        if self.plt:
            self.removeItem(self.plt)
        self.plt = self.addPlot()  # pg.PlotWidget()
        self.plt.showGrid(x=True, y=True)
        # self.plt.setXRange(5,20, padding=0)
        fontcolor = "#000000"
        labelStyle = {"color": fontcolor}
        self.plt.setLabel("left", unit=unit, **labelStyle)
        self.plt.setLabel("bottom", "Zeit", "s", **labelStyle)
        self.plt.axes["bottom"]["item"].style["showValues"] = False
        self.setBackground("w")
        # pen=pg.mkPen(color=colors[i - 1]),
        if self.smooth_data:
            self.curve = self.plt.plot(self.x, rolling_average(self.y, 50), self.color)
        else:
            self.curve = self.plt.plot(
                self.x,
                self.y,
                self.color,
            )

        # QTimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.update = True
        if self.mqtt_config:
            self.client = init_mqtt(
                mqtt_config,
                mqtt_topics=["time_data"],
                client_name="MeasurementGUI_plot_subscriber",
                on_message_func=[self.updateplot],
            )

    def start_update_routine(self, datagenerator, channel) -> None:
        self.update = True
        self.channel = channel
        self.datagenerator = datagenerator
        # if self.curve:
        #     self.plt.removeItem(self.curve)
        # reinit the deque to remove old data from the plot
        self.databuffer = collections.deque([0.0] * self.x.size, self.x.size)
        self.timer.start(self.display_interval)

    def stop_update_routine(self) -> None:
        self.timer.stop()
        if self.client:
            self.client.disconnect()
        self.update = False

    def reset_plot(self) -> None:
        self.datagenerator = None
        self.last_trai = 1
        self.channels_checked = False
        self.plot_init = False

    def getdata(self) -> np.ndarray:

        records = pd.DataFrame(self.datagenerator)
        if not records.empty:
            records = records.set_index("trai")
            self.check_channel(records)
            if not self.nr_blocks > 0:
                self.blocksize = records.samples.iloc[-1]
                self.nr_blocks = int(np.round(self.bufsize / self.blocksize))
            self.last_trai = records.index[-1]
            timedata = records.loc[records["channel"] == self.channel, "data"]
            timepoints = records.loc[records["channel"] == self.channel, "time"]
            timedata = timedata.iloc[-self.nr_blocks :]
            if not timedata.empty:
                timedata = np.hstack(timedata)
                # [ ] TODO numpy raise an index error if -self.bufsize exeeds the size
                # timedata = timedata[-self.bufsize :]
                if not self.timevector_updated and records.shape[0] > 1:
                    timestep = timepoints.iloc[0] - timepoints.iloc[1]
                    timestart = self.blocksize * self.nr_blocks * timestep  # timepoints has a bigger shape!
                    # [ ] Review that x_vector maybe don't use x-ticks, there may be latency and the time ticks may be not correct?
                    self.x = np.linspace(timestart, 0.0, self.blocksize * self.nr_blocks)
                    self.plt.setXRange(self.x.min(), self.x.max())
                    self.databuffer = collections.deque([0.0] * self.x.size, self.x.size)
                    self.timevector_updated = True
                # [ ] Review modifying the sql-query of the existing generator
                # [ ] TODO check if always working
                query = self.datagenerator._query.splitlines()

                if self.read_blocks:
                    query[-1] = f" WHERE (trai > {self.last_trai}) AND (trai < {self.last_trai + self.read_blocks})"
                else:
                    query[-1] = f" WHERE trai > {self.last_trai}"
                query = ("\n").join(query)
                self.datagenerator._query = query
            else:
                timedata = np.array([])
        else:
            timedata = np.array([])

        if not self.update:
            timedata = np.array([])

        return timedata

    def check_channel(self, records: pd.DataFrame) -> None:

        channels_in_db = records.channel.unique()
        if not self.channel in channels_in_db:
            # [ ] Review maybe it is better to plot nothing, because the channel in the tab window is the not existing channel
            LOGGER.info("Can not plot transient data, because the chosen channel is not in the measurement data!")
            self.stop_update_routine()
            # self.channel = channels_in_db.min()
            # LOGGER.info(f"Going to plot channel {self.channel} instead.")
        self.channels_checked = True

    def updateplot(self, plot_data: Optional[pd.DataFrame] = None):
        if not plot_data:
            timedata = self.getdata()
        else:
            timedata = plot_data["data"]
        if timedata.size > 0:
            # [ ] Review not possible to append list at once -> better to use list instead of deque?
            for el in timedata:
                self.databuffer.append(el)
            self.y = np.array(self.databuffer)

            if self.smooth_data:
                self.curve.setData(self.x, rolling_average(self.y, 50))
            else:
                self.curve.setData(self.x, self.y)
