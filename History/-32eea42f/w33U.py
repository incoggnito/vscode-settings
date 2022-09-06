"""Handle audio files"""

import logging
from pathlib import PurePath
from typing import Generator, Optional, Tuple

import numpy as np

import soundfile as sf
from scipy.signal import decimate

from .utils import BaseFile, Data

LOGGER = logging.getLogger(__name__)


class AudioFile(BaseFile):
    """Special Operations on audio files"""

    def __init__(self, file_obj: PurePath):
        """Inherit all attributes and methods from the _File Class

        supported file formats:
            'WAV':    # Microsoft WAV format (little endian default).
            'AIFF':   # Apple/SGI AIFF format (big endian).
            'AU':     # Sun/NeXT AU format (big endian).
            'RAW':    # RAW PCM data.
            'PAF':    # Ensoniq PARIS file format.
            'SVX':    # Amiga IFF / SVX8 / SV16 format.
            'NIST':   # Sphere NIST format.
            'VOC':    # VOC files.
            'IRCAM':  # Berkeley/IRCAM/CARL
            'W64':    # Sonic Foundry's 64 bit RIFF/WAV
            'MAT4':   # Matlab (tm) V4.2 / GNU Octave 2.0
            'MAT5':   # Matlab (tm) V5.0 / GNU Octave 2.1
            'PVF':    # Portable Voice Format
            'XI':     # Fasttracker 2 Extended Instrument
            'HTK':    # HMM Tool Kit format
            'SDS':    # Midi Sample Dump Standard
            'AVR':    # Audio Visual Research
            'WAVEX':  # MS WAVE with WAVEFORMATEX
            'SD2':    # Sound Designer 2
            'FLAC':   # FLAC lossless file format
            'CAF':    # Core Audio File format
            'WVE':    # Psion WVE format
            'OGG':    # Xiph OGG container
            'MPC2K':  # Akai MPC 2000 sampler
            'RF64':   # RF64 WAV file


        """
        super().__init__(file_obj)
        self._check_filetypes(
            (
                ".wav",
                ".flac",
                ".ogg",
                ".oga",
                ".ogv",
                ".ogx",
                ".aiff",
                ".au",
                ".raw",
                ".paf",
                ".svx",
                ".nist",
                ".voc",
                ".ircam",
                ".w64",
                ".mat4",
                ".mat5",
                ".pvf",
                ".xi",
                ".htk",
                ".sds",
                ".avr",
                ".wavex",
                ".sd2",
                ".caf",
                ".wve",
                ".mpc2k",
                ".rf64",
            )
        )

        # [ ] TODO add here all filetype, supported by http://www.mega-nerd.com/libsndfile/#Features
        # [ ] TODO libsndfile can also read/write mat files containig audio data (how to handle that)
        # -> mat files can contain other data aswell
        # [ ] TODO mp3 is not supported due to patent concerns
        self.data = Data
        self.samplefrequency = float()
        self.samples = int()  # [ ] TODO empty init of variable type so okay?
        self.data.x = np.array([])

    def read(self) -> None:
        """Reads the audio file:
        self.data -> data of the audiofile
        self.samplefrequency -> samplefrequency of the audiofile"""
        self.data, self.samplefrequency = sf.read(self.path)

    def write(
        self,
        data: np.ndarray,
        fs: int,
        max_amplitude: Optional[float] = None,
        compressor_threshold: float = 0,
        compressor_ratio: int = 1,
        decimation: int = 1,
        speed: float = 1.0,
    ) -> None:
        """Write (time) data to audio file.

        Args:
            data (np.ndarray): array with the timedata
            fs (int): samplefrequency of the original data
            max_amplitude: Maximum amplitude for normalization.
                Maps to [-1, 1] in the wav audio file.
                `None` will use peak amplitude in signal.
            compressor_threshold: Compressor threshold in Decibel (0 dB -> max. amplitude).
                A threshold of -6 dB will compress all amplitudes above 50 % of the max amplitude.
            compressor_ratio: Ratio between uncompressed input and compressed output above threshold.
            decimation: Decimation factor (>= 1).
                The resulting sampling rate will be the original rate divided by the decimation factor.
            speed: Playback speed (< 1: slower, > 1: faster).
                Reduce playback speed to make high frequencies audible.

        :raises:
            ValueError: soundfile may rise an error format not recogniced, of if the data is in the wrong
                format (has to be (x,) and not (x,1) -> use .squeeze() if necessary)
            ValueError: if the signal is empty
        """
        # [ ] TODO pylint complains about not documented Value Errors...
        # [ ] REVIEW write the self.data to file or pass the data as input argument?
        LOGGER.info("Start audio extraction...")
        LOGGER.info("Audio:                %s", self.shortname)
        LOGGER.info("Compressor threshold: %f dB", compressor_threshold)
        LOGGER.info("Compressor ratio:     %d:1", compressor_ratio)
        LOGGER.info("Decimation:           %d", decimation)
        LOGGER.info("Speed                 %f", speed)

        audio_format = self.file_type
        formats = {".wav", ".flac"}
        if audio_format not in formats:  # [ ] TODO maybe this filetype check is obsolent
            raise ValueError(f"Invalid audio format {audio_format}. Following formats are allowed: {formats}")

        if not data.size:
            raise ValueError("Signal is empty")

        LOGGER.info("Samplerate original: %d Hz", fs)

        # # decimate signal
        # if decimation > 1:
        #     decimation = int(decimation)
        #     fs = int(fs / decimation)
        #     LOGGER.info("Samplerate decimated: %d Hz", fs)
        #     # multiple decimations for factors > 13
        #     # https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.decimate.html
        #     decimation_factors = self._find_integer_divisors(decimation, 13)
        #     for factor in decimation_factors:
        #         LOGGER.info("Decimate signal by factor %d", factor)
        #         y = decimate(data, factor, zero_phase=False)
        # else:
        #     y = data

        # use compressor to dampen high amplitudes
        if compressor_threshold < 0 and compressor_ratio > 1:
            LOGGER.info("Compress signal with %f dB threshold and %f:1 ratio", compressor_threshold, compressor_ratio)
            y = self._compress(y, compressor_threshold, compressor_ratio)

        # normalize amplitudes to [-1; 1]
        max_amplitude_signal = np.max(np.abs(y))
        if max_amplitude is None:
            max_amplitude = max_amplitude_signal
        LOGGER.info("Normalize to %0.4f V (max. amplitude in signal: %0.4f V)", max_amplitude, max_amplitude_signal)
        y /= max_amplitude
        np.clip(y, -1, 1)

        # calculate samplerate for given speed
        fs = int(fs * speed)
        LOGGER.info("Samplerate output: %d Hz", fs)

        LOGGER.info("Write audio file...")
        sf.write(self.path, y, samplerate=fs, subtype="PCM_16")

    @staticmethod
    def _most_equal_divisors(number: int) -> Tuple[int, int]:
        for divisor1 in range(2, number):
            if not number % divisor1:  # pylint don't like comparision to zero
                divisor2 = number // divisor1
                if divisor1 > divisor2:
                    return divisor1, divisor2
        return 1, number

    def _find_integer_divisors(self, number: int, max_value: int) -> Generator:
        divisor1, divisor2 = self._most_equal_divisors(number)
        if divisor1 == 1 or divisor2 == 1:
            yield number
            return
        for divisor in (divisor1, divisor2):
            if divisor > max_value:
                yield from self._find_integer_divisors(divisor, max_value)
            elif divisor > 1:
                yield divisor

    @staticmethod
    def _compress(signal: np.ndarray, threshold_decibel: float, ratio: int) -> np.ndarray:
        result = signal.copy()
        max_amplitude_signal = np.max(np.abs(signal))
        threshold_amplitude = max_amplitude_signal * 10 ** (threshold_decibel / 20)
        mask = np.abs(signal) > threshold_amplitude
        sign = np.sign(signal)
        result[mask] = sign[mask] * (threshold_amplitude + (np.abs(result)[mask] - threshold_amplitude) / ratio)
        return result
