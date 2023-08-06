from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spectrum:
	"""Spectrum commands group definition. 31 total commands, 6 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spectrum", core, parent)

	@property
	def tgenerator(self):
		"""tgenerator commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tgenerator'):
			from .Tgenerator import Tgenerator
			self._tgenerator = Tgenerator(self._core, self._cmd_group)
		return self._tgenerator

	@property
	def zeroSpan(self):
		"""zeroSpan commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_zeroSpan'):
			from .ZeroSpan import ZeroSpan
			self._zeroSpan = ZeroSpan(self._core, self._cmd_group)
		return self._zeroSpan

	@property
	def frequency(self):
		"""frequency commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import Frequency
			self._frequency = Frequency(self._core, self._cmd_group)
		return self._frequency

	@property
	def freqSweep(self):
		"""freqSweep commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_freqSweep'):
			from .FreqSweep import FreqSweep
			self._freqSweep = FreqSweep(self._core, self._cmd_group)
		return self._freqSweep

	@property
	def vswr(self):
		"""vswr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_vswr'):
			from .Vswr import Vswr
			self._vswr = Vswr(self._core, self._cmd_group)
		return self._vswr

	@property
	def marker(self):
		"""marker commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import Marker
			self._marker = Marker(self._core, self._cmd_group)
		return self._marker

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.AveragingMode:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:AMODe \n
		Snippet: value: enums.AveragingMode = driver.configure.gprfMeasurement.spectrum.get_amode() \n
		Defines how the average trace is derived from the current trace. \n
			:return: averaging_mode: LINear | LOGarithmic LINear Averaging of the linear powers LOGarithmic Averaging of the dBm values
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.AveragingMode)

	def set_amode(self, averaging_mode: enums.AveragingMode) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:AMODe \n
		Snippet: driver.configure.gprfMeasurement.spectrum.set_amode(averaging_mode = enums.AveragingMode.LINear) \n
		Defines how the average trace is derived from the current trace. \n
			:param averaging_mode: LINear | LOGarithmic LINear Averaging of the linear powers LOGarithmic Averaging of the dBm values
		"""
		param = Conversions.enum_scalar_to_str(averaging_mode, enums.AveragingMode)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:AMODe {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.gprfMeasurement.spectrum.get_repetition() \n
		Selects whether the measurement is repeated continuously or not. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:REPetition \n
		Snippet: driver.configure.gprfMeasurement.spectrum.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Selects whether the measurement is repeated continuously or not. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:REPetition {param}')

	def get_rcoupling(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:RCOupling \n
		Snippet: value: bool = driver.configure.gprfMeasurement.spectrum.get_rcoupling() \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:return: repetition_coupl: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:RCOupling?')
		return Conversions.str_to_bool(response)

	def set_rcoupling(self, repetition_coupl: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:RCOupling \n
		Snippet: driver.configure.gprfMeasurement.spectrum.set_rcoupling(repetition_coupl = False) \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:param repetition_coupl: OFF | ON
		"""
		param = Conversions.bool_to_str(repetition_coupl)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:RCOupling {param}')

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TOUT \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: tcd_timeout: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_timeout: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TOUT \n
		Snippet: driver.configure.gprfMeasurement.spectrum.set_timeout(tcd_timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param tcd_timeout: Unit: s
		"""
		param = Conversions.decimal_value_to_str(tcd_timeout)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TOUT {param}')

	def get_scount(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:SCOunt \n
		Snippet: value: int = driver.configure.gprfMeasurement.spectrum.get_scount() \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval covers the frequency span
		defined for the 'Frequency Sweep' mode, or the sweep time defined for the 'Zero Span' mode. \n
			:return: statistic_count: Range: 1 to 1000
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:SCOunt \n
		Snippet: driver.configure.gprfMeasurement.spectrum.set_scount(statistic_count = 1) \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval covers the frequency span
		defined for the 'Frequency Sweep' mode, or the sweep time defined for the 'Zero Span' mode. \n
			:param statistic_count: Range: 1 to 1000
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:SCOunt {param}')

	def clone(self) -> 'Spectrum':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Spectrum(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
