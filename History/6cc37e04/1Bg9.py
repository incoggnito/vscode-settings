"""Handle Polytec Files"""
import logging
from pathlib import PurePath
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from pythoncom import com_error  # pylint: disable=no-name-in-module
from win32com.client import CDispatch, Dispatch

from atoolbox.utils import BaseFile, Data, Geometry

LOGGER = logging.getLogger(__name__)


class PolyFile(BaseFile):
    """Class to handle polytec ftypes."""

    # pylint: disable=attribute-defined-outside-init

    def __init__(self, file_obj: PurePath) -> None:
        """Inherit all attributes and methods from the _File Class"""
        super().__init__(file_obj)
        self._check_filetypes((".svd", ".pvd"))

    def read(
        self,
        *,
        pointdomain: Union[str, None] = None,
        channel: Union[str, None] = None,
        signal: Union[str, None] = None,
        display: Union[str, None] = None,
        point: int = 0,
        frame: int = 0,
        meta_only: bool = False,
    ) -> Data:
        """Read specific measurement data from a polytec file.

        Args:
            pointdomain: Domäne (Zeit, FFT, Terzen)
            channel: Kanal (Vib3D, Ref21, ..)
            signal: Signal (Weg, Geschwindigkeit, Beschleunigung, ...)
            display: Display (Amplitude, Phase, Imaginär,...)
            point: Filter a specific datapoint (0=All)
            frame: Filter a frame
            meta_only: Get only meta information

        Return:
            data [Data]: The data object
        """
        self.pointdomain = pointdomain
        self.channel = channel
        self.signal = signal
        self.display = display
        self.point = point
        self.frame = frame
        self.meta_only = meta_only
        self.settings: Dict[str, List[Optional[str]]] = {}
        self.data = Data()
        self.geometry = Geometry()

        self._open()
        self._get_pointdomain()
        self._get_channel()
        self._get_signal()
        self._get_display()

        if not meta_only:
            self._get_datapoints()
            if not hasattr(self, "element_indices"):
                self._get_geometry()
        # try:
        #     self._get_banddomains()
        # except:
        #     LOGGER.info("No banddomain found!")

        return self.data

    def write(self) -> None:
        """Write stuff"""
        raise NotImplementedError("It's currently not supported to create Polytec files")

    @staticmethod
    def _get_collection_item(i: int, collection: CDispatch) -> Any:
        try:
            item = collection.Item(int(i + 1)).Name
        except com_error as e:
            logging.error(e)
            item = None

        return item

    def _get_attr_poly(self, collection: CDispatch) -> List[Optional[str]]:
        """Helper to collect attributes in a specific collection"""
        attrs = []
        for i in range(collection.Count):
            attrs.append(self._get_collection_item(i, collection))
        attrs = [a for a in attrs if attrs]
        return attrs

    def _open(self) -> None:
        """Open the poly file"""
        try:
            self.__com_obj__ = Dispatch("PolyFile.PolyFile")
        except Exception as e:
            LOGGER.exception(e)
            self.__com_obj__.close()
            raise

        try:
            self.__com_obj__.open(str(self.path))
        except Exception as e:
            LOGGER.error(e)
            raise

    def _get_attr(
        self,
        fname: str,
        com_obj: CDispatch,
        preselection: Union[str, None] = None,
    ) -> Tuple[CDispatch, Optional[str]]:
        """Get the attributes from a com dispatch object"""
        attrs = self._get_attr_poly(com_obj)
        self.settings[f"{fname}s"] = attrs
        if preselection is None:
            for i, el in enumerate(attrs):
                print(i, el)
            sel = int(input("Please select a number!"))
            return com_obj.Item(attrs[sel]), attrs[sel]
        return com_obj.Item(preselection), preselection

    def _get_pointdomain(self) -> None:
        """Get the point domain"""
        try:
            self.__pointdomain__, self.pointdomain = self._get_attr(
                "pointdomain", self.__com_obj__.GetPointDomains(), self.pointdomain
            )
        except Exception as e:
            LOGGER.exception(e)
            raise

    def _get_channel(self) -> None:
        """Get the channel"""
        try:
            self.__channel__, self.channel = self._get_attr("channel", self.__pointdomain__.Channels, self.channel)
        except Exception as e:
            LOGGER.exception(e)
            raise

    def _get_signal(self) -> None:
        """Get the signal"""

        try:
            self.__signal__, self.signal = self._get_attr("signal", self.__channel__.Signals, self.signal)
        except Exception as e:
            LOGGER.exception(e)
            raise

        self.data.is_complex = self.__signal__.Description.Complex
        xaxis = self.__signal__.Description.XAxis
        self.data.x = np.arange(xaxis.Min, xaxis.Max, (xaxis.Max - xaxis.Min) / (xaxis.MaxCount))

    def _get_display(self) -> None:
        """Get the display"""
        try:
            self.__display__, self.display = self._get_attr("display", self.__signal__.Displays, self.display)
        except Exception as e:
            LOGGER.exception(e)
            raise

    def _get_datapoints(self) -> None:
        """Get all datapoints"""
        try:
            __datapoints__ = self.__pointdomain__.datapoints
        except Exception as e:
            LOGGER.exception(e)
            raise

        if not self.point:  # get all measurement points
            y = []
            for i in range(1, __datapoints__.count + 1):
                datapoint = __datapoints__.Item(i)
                # datapoint.MeasPoint.Index
                # datapoint.MeasPoint.Label
                # datapoint.GetScanStatus(self.__display__)
                if not isinstance(self.__channel__.caps, str):
                    ytemp = datapoint.GetData(self.__display__, self.frame)
                    if len(ytemp) > 0:
                        y.append(ytemp)

                else:
                    ytemp = datapoint.GetData(self.__display__, self.frame)
                    y.append(ytemp)
            y2 = np.array(y, np.float32)  # TODO, dtype=np.float16)

            # handle complex data
            if self.data.is_complex == 1 and self.__display__.Type == 9:
                real_data = y2[:, 0::2]
                imag_data = y2[:, 1::2]
                y2 = np.vectorize(complex)(real_data, imag_data)

        else:
            datapoint = __datapoints__.Item(self.point)
            y2 = np.asarray(datapoint.GetData(self.__display__, self.frame))

            # handle complex data
            if self.data.is_complex == 1 and self.__display__.Type == 9:
                real_data = y2[0::2]
                imag_data = y2[1::2]
                y2 = np.vectorize(complex, otypes=np.float32)(real_data, imag_data)

        self.data.y = y2

    @staticmethod
    def _get_3D_bands(channels: dict, DomainBand) -> dict:
        """Get each band dataset for 3D Mode and combine it with the peak"""
        displaybands = {}
        for key, data in channels.items():
            if data.Signals.Exists("Velocity"):
                signal = data.Signals("Velocity")
            else:
                signal = data.Signals.Item(3)
            if signal.Description.Complex:
                displaybands[key] = signal.Displays.Type(9)  # Real & Imag
            else:
                displaybands[key] = signal.Displays.Type(1)

        Data = {}
        for DataBand in DomainBand.GetDataBands(displaybands[key].Signal):
            data = []
            for key, displayband in displaybands.items():
                if signal.Description.Complex:
                    arr = np.array(DataBand.GetData(displayband, 0))  # .reshape(1, -1)
                    real_data = arr[::2]
                    imag_data = arr[1::2]
                    arr = np.vectorize(complex)(real_data, imag_data)  # .reshape(-1)
                else:
                    arr = np.array(DataBand.GetData(displayband, 0))
                data.append(arr)

            shaped_data = []
            for i in range(0, len(data[0])):
                # Calculate the magnitude for 3D data
                shaped_data.append([data[0][i], data[1][i], data[2][i]])
            shapped_data = np.array(shaped_data)
            Data[DataBand.Peak] = shapped_data
        return Data

    @staticmethod
    def _get_1D_bands(channel, DomainBand):
        if channel.Signals.Exsists("Velocity"):
            # To find Items name Signals.Item(1).Name and Signals.Count
            SignalBand = channel.Signals("Velocity")
        else:
            SignalBand = channel.Signals.Item(3)

        DisplayBand = SignalBand.Displays.Type(1)

        Data = {}
        for DataBand in DomainBand.GetDataBands(DisplayBand.Signal):
            data = DataBand.GetData(DisplayBand, 0)
            Data[DataBand.Peak] = data
        return Data

    def _get_banddomains(self, ref: str):
        self._open()
        try:
            BandDomains = self.__com_obj__.GetBandDomains(592703)
        except Exception as e:
            LOGGER.warning(e, "In files of this type there are no band domains.")
        else:
            if not BandDomains.Exists(3):
                LOGGER.info("INFO: No bands defined in the file.")

        DomainBand = BandDomains.Type(3)
        # Check if the file is 1D or 3D
        Is1D = DomainBand.Channels.Exists("Vib")
        Is3D = (
            DomainBand.Channels.Exists("Vib X")
            and DomainBand.Channels.Exists("Vib Y")
            and DomainBand.Channels.Exists("Vib Z")
        )
        dirs = ["X", "Y", "Z"]
        # Assign channels for the file and check if there is velocity data present
        if Is1D:
            channel = DomainBand.Channels("Vib")
            frf_channel = DomainBand.Cannels(f"Vib & {ref}")
            VelocityExists = channel.Signals.Exists("Velocity")
        elif Is3D:
            channels, frf_channels = {}, {}
            for ch in dirs:
                channels[ch] = DomainBand.Channels(f"Vib {ch}")
                frf_channels[f"FRF_{ch}"] = DomainBand.Channels(f"Vib {ch} & {ref}")
                VelocityExists = channels["X"].Signals.Exists("Velocity")
        else:
            VelocityExists = False

        # Return a list of data sets containing the band data for either a 1D or a
        # 3D file - for 3D data, the resulting magnitude must additionally
        # be calculated
        if VelocityExists and Is3D:
            Data = self._get_3D_bands(channels, DomainBand)
            frf_Data = self._get_3D_bands(frf_channels, DomainBand)

        elif VelocityExists and Is1D:
            Data = self._get_1D_bands(channel, DomainBand)
            frf_Data = self._get_1D_bands(frf_channel, DomainBand)
        else:
            pass

        self.banddata = Data
        self.frf_banddata = frf_Data

    def _get_geometry(self) -> None:
        """Get the coordinates of the points and the element groupings"""
        try:
            measpoints = self.__com_obj__.Infos.MeasPoints
        except Exception as e:
            LOGGER.exception(e)
            raise

        if not self.point:
            # Delte Scanpoints without Status
            coordinates, xyz = zip(*[((m.Index, m.ScanStatus), (m.Index, *m.CoordXYZ())) for m in measpoints])
            xyz = np.array(xyz)
            elements = self.__com_obj__.Infos.Elements
            el_inds = np.zeros((elements.count, 4))
            for i, el in enumerate(elements):
                xfill = 3 - len(el.MeasPointIndices)
                mpoints = xfill * [0] + list(el.MeasPointIndices)
                el_inds[i, :] = np.array((i, *mpoints))

            al_points = self.__com_obj__.Infos.Alignments.Alignments3D.Item(1).Align3DPoints
            alp = np.array([(al.X, al.Y, al.Z) for al in al_points])
        if xyz.size > 0:
            self.geometry.xyz = xyz
        if el_inds.size > 0:
            self.geometry.elements = el_inds
        if alp.size > 0:
            if (alp.shape[0] >= 5) and alp.ndim > 1:
                self.geometry.ref_points = alp[:5, :]
        if len(coordinates) > 0:
            self.geometry.status = np.array(coordinates)


def read_fft(file: PolyFile, channel: str, channel_unit: str) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
    """Read fft from polyfile"""
    try:
        file.read(
            pointdomain="FFT",
            channel=str(channel),
            signal=channel_unit,
            display="Real & Imag.",
        )
    except com_error as e:
        file.read(
            pointdomain="FFT",
            channel=str(channel),
            signal=channel_unit,
            display="Amplitude",
        )
        LOGGER.warning(" ".join([e.args[1], f"|Input:-> read_fft ->({channel}, FFT, {channel_unit}, Real & Imag.)"]))

    return (file.data.x, file.data.y)


def read_frf(file: PolyFile, ref: str, ref_unit: str, channel: str, channel_unit: str) -> Optional[np.ndarray]:
    """Read the FRF from a reference"""
    try:
        file.read(
            pointdomain="FFT",
            channel=f"{channel} & {ref}",
            signal=f"H1 {channel_unit} / {ref_unit}",
            display="Real & Imag.",
        )
    except com_error as e:
        LOGGER.warning(
            " ".join(
                [
                    e.args[1],
                    f"| Input:-> read_frf -> (FRF_{channel} & {ref}, FFT, H1",
                    f"{channel_unit} / {ref_unit}, Real & Imag.)",
                ]
            ),
        )
    return file.data.y


def read_coherence(file: PolyFile, ref: str, channel: str) -> Optional[np.ndarray]:
    """Read the coherence from file"""
    try:
        file.read(
            pointdomain="FFT",
            channel=f"{channel} & {ref}",
            signal="Kohärenz",
            display="Amplitude",
        )
    except com_error as e:
        LOGGER.warning(
            " ".join(
                [e.args[1], f"| Input:-> read_coherence -> (COH_{channel} & {ref}", ", FFT, Kohärenz Amplitude)"]
            ),
        )
    return file.data.y
