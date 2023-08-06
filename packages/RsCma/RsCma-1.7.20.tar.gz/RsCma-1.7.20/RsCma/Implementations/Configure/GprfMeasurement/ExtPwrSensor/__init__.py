from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ExtPwrSensor:
	"""ExtPwrSensor commands group definition. 9 total commands, 2 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("extPwrSensor", core, parent)

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_average'):
			from .Average import Average
			self._average = Average(self._core, self._cmd_group)
		return self._average

	@property
	def attenuation(self):
		"""attenuation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_attenuation'):
			from .Attenuation import Attenuation
			self._attenuation = Attenuation(self._core, self._cmd_group)
		return self._attenuation

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:TOUT \n
		Snippet: value: float = driver.configure.gprfMeasurement.extPwrSensor.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: tcd_timeout: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_timeout: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:TOUT \n
		Snippet: driver.configure.gprfMeasurement.extPwrSensor.set_timeout(tcd_timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param tcd_timeout: Unit: s
		"""
		param = Conversions.decimal_value_to_str(tcd_timeout)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:TOUT {param}')

	# noinspection PyTypeChecker
	def get_resolution(self) -> enums.ExtSensorResolution:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:RESolution \n
		Snippet: value: enums.ExtSensorResolution = driver.configure.gprfMeasurement.extPwrSensor.get_resolution() \n
		Defines the number of decimal places of the power results displayed in the graphical user interface. This command does
		not affect results queried via remote control commands. \n
			:return: resolution: PD0 | PD1 | PD2 | PD3 PDn Results rounded to n places after the decimal point
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:RESolution?')
		return Conversions.str_to_scalar_enum(response, enums.ExtSensorResolution)

	def set_resolution(self, resolution: enums.ExtSensorResolution) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:RESolution \n
		Snippet: driver.configure.gprfMeasurement.extPwrSensor.set_resolution(resolution = enums.ExtSensorResolution.PD0) \n
		Defines the number of decimal places of the power results displayed in the graphical user interface. This command does
		not affect results queried via remote control commands. \n
			:param resolution: PD0 | PD1 | PD2 | PD3 PDn Results rounded to n places after the decimal point
		"""
		param = Conversions.enum_scalar_to_str(resolution, enums.ExtSensorResolution)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:RESolution {param}')

	def get_scount(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:SCOunt \n
		Snippet: value: int = driver.configure.gprfMeasurement.extPwrSensor.get_scount() \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval comprises one power result
		requested from the power sensor. \n
			:return: statistic_count: Range: 1 to 1000
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:SCOunt \n
		Snippet: driver.configure.gprfMeasurement.extPwrSensor.set_scount(statistic_count = 1) \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval comprises one power result
		requested from the power sensor. \n
			:param statistic_count: Range: 1 to 1000
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:SCOunt {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.gprfMeasurement.extPwrSensor.get_repetition() \n
		Selects whether the measurement is repeated continuously or not. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:REPetition \n
		Snippet: driver.configure.gprfMeasurement.extPwrSensor.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Selects whether the measurement is repeated continuously or not. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:REPetition {param}')

	def get_rcoupling(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:RCOupling \n
		Snippet: value: bool = driver.configure.gprfMeasurement.extPwrSensor.get_rcoupling() \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:return: repetition_coupl: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:RCOupling?')
		return Conversions.str_to_bool(response)

	def set_rcoupling(self, repetition_coupl: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:RCOupling \n
		Snippet: driver.configure.gprfMeasurement.extPwrSensor.set_rcoupling(repetition_coupl = False) \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:param repetition_coupl: OFF | ON
		"""
		param = Conversions.bool_to_str(repetition_coupl)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:RCOupling {param}')

	def get_frequency(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:FREQuency \n
		Snippet: value: float = driver.configure.gprfMeasurement.extPwrSensor.get_frequency() \n
		Specifies the input frequency at the power sensor. \n
			:return: correction_freq: Range: Depends on used sensor model , Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, correction_freq: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:FREQuency \n
		Snippet: driver.configure.gprfMeasurement.extPwrSensor.set_frequency(correction_freq = 1.0) \n
		Specifies the input frequency at the power sensor. \n
			:param correction_freq: Range: Depends on used sensor model , Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(correction_freq)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:FREQuency {param}')

	def clone(self) -> 'ExtPwrSensor':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ExtPwrSensor(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
