from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FftSpecAn:
	"""FftSpecAn commands group definition. 13 total commands, 2 Subgroups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fftSpecAn", core, parent)

	@property
	def peakSearch(self):
		"""peakSearch commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_peakSearch'):
			from .PeakSearch import PeakSearch
			self._peakSearch = PeakSearch(self._core, self._cmd_group)
		return self._peakSearch

	@property
	def marker(self):
		"""marker commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import Marker
			self._marker = Marker(self._core, self._cmd_group)
		return self._marker

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:TOUT \n
		Snippet: value: float = driver.configure.gprfMeasurement.fftSpecAn.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: tcd_timeout: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_timeout: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:TOUT \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.set_timeout(tcd_timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param tcd_timeout: Unit: s
		"""
		param = Conversions.decimal_value_to_str(tcd_timeout)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:TOUT {param}')

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.AveragingMode:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:AMODe \n
		Snippet: value: enums.AveragingMode = driver.configure.gprfMeasurement.fftSpecAn.get_amode() \n
		Defines how the average FFT trace is derived from the current trace. \n
			:return: averaging_mode: LINear | LOGarithmic LINear Averaging of the linear powers LOGarithmic Averaging of the dBm values
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.AveragingMode)

	def set_amode(self, averaging_mode: enums.AveragingMode) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:AMODe \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.set_amode(averaging_mode = enums.AveragingMode.LINear) \n
		Defines how the average FFT trace is derived from the current trace. \n
			:param averaging_mode: LINear | LOGarithmic LINear Averaging of the linear powers LOGarithmic Averaging of the dBm values
		"""
		param = Conversions.enum_scalar_to_str(averaging_mode, enums.AveragingMode)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:AMODe {param}')

	# noinspection PyTypeChecker
	def get_detector(self) -> enums.DetectorSimple:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:DETector \n
		Snippet: value: enums.DetectorSimple = driver.configure.gprfMeasurement.fftSpecAn.get_detector() \n
		Defines how a spectrum diagram point is calculated from adjacent frequency domain samples. \n
			:return: detector: PEAK | RMS PEAK The sample with the largest power is displayed. RMS The RMS value of the samples is displayed.
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:DETector?')
		return Conversions.str_to_scalar_enum(response, enums.DetectorSimple)

	def set_detector(self, detector: enums.DetectorSimple) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:DETector \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.set_detector(detector = enums.DetectorSimple.PEAK) \n
		Defines how a spectrum diagram point is calculated from adjacent frequency domain samples. \n
			:param detector: PEAK | RMS PEAK The sample with the largest power is displayed. RMS The RMS value of the samples is displayed.
		"""
		param = Conversions.enum_scalar_to_str(detector, enums.DetectorSimple)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:DETector {param}')

	def get_fft_length(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:FFTLength \n
		Snippet: value: int = driver.configure.gprfMeasurement.fftSpecAn.get_fft_length() \n
		Specifies the number of samples used for the FFT analysis. \n
			:return: length: You can enter values between 1024 and 16384. The setting is rounded to the closest integer power of two.
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:FFTLength?')
		return Conversions.str_to_int(response)

	def set_fft_length(self, length: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:FFTLength \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.set_fft_length(length = 1) \n
		Specifies the number of samples used for the FFT analysis. \n
			:param length: You can enter values between 1024 and 16384. The setting is rounded to the closest integer power of two.
		"""
		param = Conversions.decimal_value_to_str(length)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:FFTLength {param}')

	def get_fspan(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:FSPan \n
		Snippet: value: float = driver.configure.gprfMeasurement.fftSpecAn.get_fspan() \n
		Defines the frequency range to be measured and thus the x-axis of the spectrum result diagram. \n
			:return: frequency_span: You can enter values between 10 kHz and 20 MHz. The setting is rounded to the closest of the following values: 10 / 20 / 40 / 80 / 160 / 320 / 640 kHz 1.25 / 2.5 / 5 / 10 / 20 MHz Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:FSPan?')
		return Conversions.str_to_float(response)

	def set_fspan(self, frequency_span: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:FSPan \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.set_fspan(frequency_span = 1.0) \n
		Defines the frequency range to be measured and thus the x-axis of the spectrum result diagram. \n
			:param frequency_span: You can enter values between 10 kHz and 20 MHz. The setting is rounded to the closest of the following values: 10 / 20 / 40 / 80 / 160 / 320 / 640 kHz 1.25 / 2.5 / 5 / 10 / 20 MHz Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency_span)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:FSPan {param}')

	def get_mo_exception(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:MOEXception \n
		Snippet: value: bool = driver.configure.gprfMeasurement.fftSpecAn.get_mo_exception() \n
		Specifies whether measurement results that the R&S CMA180 identifies as faulty or inaccurate are rejected. \n
			:return: meas_on_exception: OFF | ON OFF Faulty results are rejected ON Results are never rejected
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:MOEXception?')
		return Conversions.str_to_bool(response)

	def set_mo_exception(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:MOEXception \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.set_mo_exception(meas_on_exception = False) \n
		Specifies whether measurement results that the R&S CMA180 identifies as faulty or inaccurate are rejected. \n
			:param meas_on_exception: OFF | ON OFF Faulty results are rejected ON Results are never rejected
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:MOEXception {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.gprfMeasurement.fftSpecAn.get_repetition() \n
		Selects whether the measurement is repeated continuously or not. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:REPetition \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Selects whether the measurement is repeated continuously or not. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:REPetition {param}')

	def get_rcoupling(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:RCOupling \n
		Snippet: value: bool = driver.configure.gprfMeasurement.fftSpecAn.get_rcoupling() \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:return: repetition_coupl: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:RCOupling?')
		return Conversions.str_to_bool(response)

	def set_rcoupling(self, repetition_coupl: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:RCOupling \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.set_rcoupling(repetition_coupl = False) \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:param repetition_coupl: OFF | ON
		"""
		param = Conversions.bool_to_str(repetition_coupl)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:RCOupling {param}')

	def get_scount(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:SCOunt \n
		Snippet: value: int = driver.configure.gprfMeasurement.fftSpecAn.get_scount() \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval comprises the number of
		samples defined by the 'FFT Length'. \n
			:return: statistic_count: Range: 1 to 1000
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:SCOunt \n
		Snippet: driver.configure.gprfMeasurement.fftSpecAn.set_scount(statistic_count = 1) \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval comprises the number of
		samples defined by the 'FFT Length'. \n
			:param statistic_count: Range: 1 to 1000
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:FFTSanalyzer:SCOunt {param}')

	def clone(self) -> 'FftSpecAn':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FftSpecAn(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
