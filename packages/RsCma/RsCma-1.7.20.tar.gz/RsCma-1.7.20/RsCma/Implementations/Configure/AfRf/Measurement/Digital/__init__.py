from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Digital:
	"""Digital commands group definition. 46 total commands, 7 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("digital", core, parent)

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_result'):
			from .Result import Result
			self._result = Result(self._core, self._cmd_group)
		return self._result

	@property
	def sync(self):
		"""sync commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sync'):
			from .Sync import Sync
			self._sync = Sync(self._core, self._cmd_group)
		return self._sync

	@property
	def rf(self):
		"""rf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import Rf
			self._rf = Rf(self._core, self._cmd_group)
		return self._rf

	@property
	def ttl(self):
		"""ttl commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_ttl'):
			from .Ttl import Ttl
			self._ttl = Ttl(self._core, self._cmd_group)
		return self._ttl

	@property
	def dmr(self):
		"""dmr commands group. 0 Sub-classes, 9 commands."""
		if not hasattr(self, '_dmr'):
			from .Dmr import Dmr
			self._dmr = Dmr(self._core, self._cmd_group)
		return self._dmr

	@property
	def tetra(self):
		"""tetra commands group. 1 Sub-classes, 13 commands."""
		if not hasattr(self, '_tetra'):
			from .Tetra import Tetra
			self._tetra = Tetra(self._core, self._cmd_group)
		return self._tetra

	@property
	def limit(self):
		"""limit commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import Limit
			self._limit = Limit(self._core, self._cmd_group)
		return self._limit

	def get_scount(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:SCOunt \n
		Snippet: value: int = driver.configure.afRf.measurement.digital.get_scount() \n
		Sets the number of measurement intervals per measurement cycle. \n
			:return: statistic_count: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:SCOunt \n
		Snippet: driver.configure.afRf.measurement.digital.set_scount(statistic_count = 1) \n
		Sets the number of measurement intervals per measurement cycle. \n
			:param statistic_count: No help available
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:SCOunt {param}')

	# noinspection PyTypeChecker
	def get_standard(self) -> enums.StandardDigital:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:STANdard \n
		Snippet: value: enums.StandardDigital = driver.configure.afRf.measurement.digital.get_standard() \n
		Selects the digital standard of the measured signal. \n
			:return: standard: DMR | TETRa
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.StandardDigital)

	def set_standard(self, standard: enums.StandardDigital) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:STANdard \n
		Snippet: driver.configure.afRf.measurement.digital.set_standard(standard = enums.StandardDigital.DMR) \n
		Selects the digital standard of the measured signal. \n
			:param standard: DMR | TETRa
		"""
		param = Conversions.enum_scalar_to_str(standard, enums.StandardDigital)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:STANdard {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.afRf.measurement.digital.get_repetition() \n
		Selects whether the measurement is repeated continuously or not. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after the statistic count. CONTinuous Continuous measurement, running until explicitly terminated.
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:REPetition \n
		Snippet: driver.configure.afRf.measurement.digital.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Selects whether the measurement is repeated continuously or not. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after the statistic count. CONTinuous Continuous measurement, running until explicitly terminated.
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:REPetition {param}')

	# noinspection PyTypeChecker
	def get_scondition(self) -> enums.StopCondition:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:SCONdition \n
		Snippet: value: enums.StopCondition = driver.configure.afRf.measurement.digital.get_scondition() \n
		Selects whether the measurement is stopped after a failed limit check or continued. \n
			:return: stop_condition: NONE | SLFail NONE Continue measurement irrespective of the limit check. SLFail Stop measurement on limit failure.
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:SCONdition?')
		return Conversions.str_to_scalar_enum(response, enums.StopCondition)

	def set_scondition(self, stop_condition: enums.StopCondition) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:SCONdition \n
		Snippet: driver.configure.afRf.measurement.digital.set_scondition(stop_condition = enums.StopCondition.NONE) \n
		Selects whether the measurement is stopped after a failed limit check or continued. \n
			:param stop_condition: NONE | SLFail NONE Continue measurement irrespective of the limit check. SLFail Stop measurement on limit failure.
		"""
		param = Conversions.enum_scalar_to_str(stop_condition, enums.StopCondition)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:SCONdition {param}')

	def get_crepetition(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:CREPetition \n
		Snippet: value: bool = driver.configure.afRf.measurement.digital.get_crepetition() \n
		Sets the repetition mode for BER measurement automatically to 'Continuous' if the local mode is used. \n
			:return: continuous_repetition: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:CREPetition?')
		return Conversions.str_to_bool(response)

	def set_crepetition(self, continuous_repetition: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:CREPetition \n
		Snippet: driver.configure.afRf.measurement.digital.set_crepetition(continuous_repetition = False) \n
		Sets the repetition mode for BER measurement automatically to 'Continuous' if the local mode is used. \n
			:param continuous_repetition: OFF | ON
		"""
		param = Conversions.bool_to_str(continuous_repetition)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:CREPetition {param}')

	def get_mo_exception(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:MOEXception \n
		Snippet: value: bool = driver.configure.afRf.measurement.digital.get_mo_exception() \n
		Specifies whether measurement results that the R&S CMA180 identifies as faulty or inaccurate are rejected. \n
			:return: meas_on_exception: OFF | ON OFF Faulty results are rejected ON Results are never rejected
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:MOEXception?')
		return Conversions.str_to_bool(response)

	def set_mo_exception(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:MOEXception \n
		Snippet: driver.configure.afRf.measurement.digital.set_mo_exception(meas_on_exception = False) \n
		Specifies whether measurement results that the R&S CMA180 identifies as faulty or inaccurate are rejected. \n
			:param meas_on_exception: OFF | ON OFF Faulty results are rejected ON Results are never rejected
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:MOEXception {param}')

	def get_rcoupling(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:RCOupling \n
		Snippet: value: bool = driver.configure.afRf.measurement.digital.get_rcoupling() \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:return: repetition_coupling: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:RCOupling?')
		return Conversions.str_to_bool(response)

	def set_rcoupling(self, repetition_coupling: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:RCOupling \n
		Snippet: driver.configure.afRf.measurement.digital.set_rcoupling(repetition_coupling = False) \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:param repetition_coupling: OFF | ON
		"""
		param = Conversions.bool_to_str(repetition_coupling)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:RCOupling {param}')

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TOUT \n
		Snippet: value: float = driver.configure.afRf.measurement.digital.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: tcd_timeout: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_timeout: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TOUT \n
		Snippet: driver.configure.afRf.measurement.digital.set_timeout(tcd_timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param tcd_timeout: Unit: s
		"""
		param = Conversions.decimal_value_to_str(tcd_timeout)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TOUT {param}')

	def clone(self) -> 'Digital':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Digital(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
