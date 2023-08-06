from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 9 total commands, 1 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	@property
	def filterPy(self):
		"""filterPy commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._cmd_group)
		return self._filterPy

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:TOUT \n
		Snippet: value: float = driver.configure.gprfMeasurement.power.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: tcd_timeout: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:POWer:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_timeout: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:TOUT \n
		Snippet: driver.configure.gprfMeasurement.power.set_timeout(tcd_timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param tcd_timeout: Unit: s
		"""
		param = Conversions.decimal_value_to_str(tcd_timeout)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:TOUT {param}')

	def get_slength(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:SLENgth \n
		Snippet: value: float = driver.configure.gprfMeasurement.power.get_slength() \n
		Sets the time between the beginning of two consecutive measurement intervals. \n
			:return: step_length: Range: 50E-6 s to 1 s, Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:POWer:SLENgth?')
		return Conversions.str_to_float(response)

	def set_slength(self, step_length: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:SLENgth \n
		Snippet: driver.configure.gprfMeasurement.power.set_slength(step_length = 1.0) \n
		Sets the time between the beginning of two consecutive measurement intervals. \n
			:param step_length: Range: 50E-6 s to 1 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(step_length)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:SLENgth {param}')

	def get_mlength(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:MLENgth \n
		Snippet: value: float = driver.configure.gprfMeasurement.power.get_mlength() \n
		Sets the time interval used to calculate one set of 'Current' power result (RMS value, minimum and maximum) . The maximum
		allowed value is limited by the step length, see method RsCma.Configure.GprfMeasurement.Power.slength. \n
			:return: meas_length: Range: 10E-6 s to StepLength, Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:POWer:MLENgth?')
		return Conversions.str_to_float(response)

	def set_mlength(self, meas_length: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:MLENgth \n
		Snippet: driver.configure.gprfMeasurement.power.set_mlength(meas_length = 1.0) \n
		Sets the time interval used to calculate one set of 'Current' power result (RMS value, minimum and maximum) . The maximum
		allowed value is limited by the step length, see method RsCma.Configure.GprfMeasurement.Power.slength. \n
			:param meas_length: Range: 10E-6 s to StepLength, Unit: s
		"""
		param = Conversions.decimal_value_to_str(meas_length)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:MLENgth {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.gprfMeasurement.power.get_repetition() \n
		Selects whether the measurement is repeated continuously or not. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:POWer:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:REPetition \n
		Snippet: driver.configure.gprfMeasurement.power.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Selects whether the measurement is repeated continuously or not. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:REPetition {param}')

	def get_rcoupling(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:RCOupling \n
		Snippet: value: bool = driver.configure.gprfMeasurement.power.get_rcoupling() \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:return: repetition_coupl: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:POWer:RCOupling?')
		return Conversions.str_to_bool(response)

	def set_rcoupling(self, repetition_coupl: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:RCOupling \n
		Snippet: driver.configure.gprfMeasurement.power.set_rcoupling(repetition_coupl = False) \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:param repetition_coupl: OFF | ON
		"""
		param = Conversions.bool_to_str(repetition_coupl)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:RCOupling {param}')

	def get_scount(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:SCOunt \n
		Snippet: value: int = driver.configure.gprfMeasurement.power.get_scount() \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval delivers one 'Current'
		power result. \n
			:return: statistic_count: Range: 1 to 100E+3
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:POWer:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:SCOunt \n
		Snippet: driver.configure.gprfMeasurement.power.set_scount(statistic_count = 1) \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval delivers one 'Current'
		power result. \n
			:param statistic_count: Range: 1 to 100E+3
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:SCOunt {param}')

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
