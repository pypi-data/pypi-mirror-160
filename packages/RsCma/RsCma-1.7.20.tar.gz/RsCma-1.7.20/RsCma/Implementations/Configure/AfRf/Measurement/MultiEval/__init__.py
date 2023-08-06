from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiEval:
	"""MultiEval commands group definition. 111 total commands, 13 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("multiEval", core, parent)

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_result'):
			from .Result import Result
			self._result = Result(self._core, self._cmd_group)
		return self._result

	@property
	def afFft(self):
		"""afFft commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_afFft'):
			from .AfFft import AfFft
			self._afFft = AfFft(self._core, self._cmd_group)
		return self._afFft

	@property
	def af(self):
		"""af commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_af'):
			from .Af import Af
			self._af = Af(self._core, self._cmd_group)
		return self._af

	@property
	def rf(self):
		"""rf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import Rf
			self._rf = Rf(self._core, self._cmd_group)
		return self._rf

	@property
	def fft(self):
		"""fft commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_fft'):
			from .Fft import Fft
			self._fft = Fft(self._core, self._cmd_group)
		return self._fft

	@property
	def tones(self):
		"""tones commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_tones'):
			from .Tones import Tones
			self._tones = Tones(self._core, self._cmd_group)
		return self._tones

	@property
	def demodulation(self):
		"""demodulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_demodulation'):
			from .Demodulation import Demodulation
			self._demodulation = Demodulation(self._core, self._cmd_group)
		return self._demodulation

	@property
	def audioInput(self):
		"""audioInput commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._cmd_group)
		return self._audioInput

	@property
	def spdifLeft(self):
		"""spdifLeft commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spdifLeft'):
			from .SpdifLeft import SpdifLeft
			self._spdifLeft = SpdifLeft(self._core, self._cmd_group)
		return self._spdifLeft

	@property
	def spdifRight(self):
		"""spdifRight commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spdifRight'):
			from .SpdifRight import SpdifRight
			self._spdifRight = SpdifRight(self._core, self._cmd_group)
		return self._spdifRight

	@property
	def limit(self):
		"""limit commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import Limit
			self._limit = Limit(self._core, self._cmd_group)
		return self._limit

	@property
	def oscilloscope(self):
		"""oscilloscope commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_oscilloscope'):
			from .Oscilloscope import Oscilloscope
			self._oscilloscope = Oscilloscope(self._core, self._cmd_group)
		return self._oscilloscope

	@property
	def filterPy(self):
		"""filterPy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._cmd_group)
		return self._filterPy

	def get_crepetition(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:CREPetition \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.get_crepetition() \n
		Enables or disables the automatic configuration of the repetition mode. With enabled automatic configuration, the
		repetition mode of all measurements is set to 'Continuous' each time the instrument switches from remote operation to
		manual operation. \n
			:return: continuous_repetition: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:CREPetition?')
		return Conversions.str_to_bool(response)

	def set_crepetition(self, continuous_repetition: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:CREPetition \n
		Snippet: driver.configure.afRf.measurement.multiEval.set_crepetition(continuous_repetition = False) \n
		Enables or disables the automatic configuration of the repetition mode. With enabled automatic configuration, the
		repetition mode of all measurements is set to 'Continuous' each time the instrument switches from remote operation to
		manual operation. \n
			:param continuous_repetition: OFF | ON
		"""
		param = Conversions.bool_to_str(continuous_repetition)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:CREPetition {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.afRf.measurement.multiEval.get_repetition() \n
		Selects whether the measurement is repeated continuously or not. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:REPetition \n
		Snippet: driver.configure.afRf.measurement.multiEval.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Selects whether the measurement is repeated continuously or not. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:REPetition {param}')

	# noinspection PyTypeChecker
	def get_scondition(self) -> enums.StopCondition:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:SCONdition \n
		Snippet: value: enums.StopCondition = driver.configure.afRf.measurement.multiEval.get_scondition() \n
		Selects whether the measurement is stopped after a failed limit check or continued. \n
			:return: stop_condition: NONE | SLFail NONE Continue measurement irrespective of the limit check SLFail Stop measurement on limit failure
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:SCONdition?')
		return Conversions.str_to_scalar_enum(response, enums.StopCondition)

	def set_scondition(self, stop_condition: enums.StopCondition) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:SCONdition \n
		Snippet: driver.configure.afRf.measurement.multiEval.set_scondition(stop_condition = enums.StopCondition.NONE) \n
		Selects whether the measurement is stopped after a failed limit check or continued. \n
			:param stop_condition: NONE | SLFail NONE Continue measurement irrespective of the limit check SLFail Stop measurement on limit failure
		"""
		param = Conversions.enum_scalar_to_str(stop_condition, enums.StopCondition)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:SCONdition {param}')

	def get_mo_exception(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:MOEXception \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.get_mo_exception() \n
		Specifies whether measurement results that the R&S CMA180 identifies as faulty or inaccurate are rejected. \n
			:return: meas_on_exception: OFF | ON OFF Faulty results are rejected ON Results are never rejected
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:MOEXception?')
		return Conversions.str_to_bool(response)

	def set_mo_exception(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:MOEXception \n
		Snippet: driver.configure.afRf.measurement.multiEval.set_mo_exception(meas_on_exception = False) \n
		Specifies whether measurement results that the R&S CMA180 identifies as faulty or inaccurate are rejected. \n
			:param meas_on_exception: OFF | ON OFF Faulty results are rejected ON Results are never rejected
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:MOEXception {param}')

	def get_rcoupling(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:RCOupling \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.get_rcoupling() \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:return: repetition_coupling: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:RCOupling?')
		return Conversions.str_to_bool(response)

	def set_rcoupling(self, repetition_coupling: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:RCOupling \n
		Snippet: driver.configure.afRf.measurement.multiEval.set_rcoupling(repetition_coupling = False) \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:param repetition_coupling: OFF | ON
		"""
		param = Conversions.bool_to_str(repetition_coupling)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:RCOupling {param}')

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: value: float = driver.configure.afRf.measurement.multiEval.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: tcd_timeout: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_timeout: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TOUT \n
		Snippet: driver.configure.afRf.measurement.multiEval.set_timeout(tcd_timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param tcd_timeout: Unit: s
		"""
		param = Conversions.decimal_value_to_str(tcd_timeout)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TOUT {param}')

	def get_sautomatic(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:SAUTomatic \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.get_sautomatic() \n
		No command help available \n
			:return: start_meas_automatic: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:SAUTomatic?')
		return Conversions.str_to_bool(response)

	def set_sautomatic(self, start_meas_automatic: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:SAUTomatic \n
		Snippet: driver.configure.afRf.measurement.multiEval.set_sautomatic(start_meas_automatic = False) \n
		No command help available \n
			:param start_meas_automatic: No help available
		"""
		param = Conversions.bool_to_str(start_meas_automatic)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:SAUTomatic {param}')

	def get_st_find(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:STFind \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.get_st_find() \n
		No command help available \n
			:return: start_find: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:STFind?')
		return Conversions.str_to_bool(response)

	def set_st_find(self, start_find: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:STFind \n
		Snippet: driver.configure.afRf.measurement.multiEval.set_st_find(start_find = False) \n
		No command help available \n
			:param start_find: No help available
		"""
		param = Conversions.bool_to_str(start_find)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:STFind {param}')

	def clone(self) -> 'MultiEval':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiEval(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
