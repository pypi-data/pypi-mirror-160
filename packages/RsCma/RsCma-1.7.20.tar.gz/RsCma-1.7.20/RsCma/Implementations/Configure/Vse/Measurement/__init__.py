from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Measurement:
	"""Measurement commands group definition. 67 total commands, 10 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("measurement", core, parent)

	@property
	def xrt(self):
		"""xrt commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_xrt'):
			from .Xrt import Xrt
			self._xrt = Xrt(self._core, self._cmd_group)
		return self._xrt

	@property
	def dmr(self):
		"""dmr commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_dmr'):
			from .Dmr import Dmr
			self._dmr = Dmr(self._core, self._cmd_group)
		return self._dmr

	@property
	def dpmr(self):
		"""dpmr commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpmr'):
			from .Dpmr import Dpmr
			self._dpmr = Dpmr(self._core, self._cmd_group)
		return self._dpmr

	@property
	def nxdn(self):
		"""nxdn commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_nxdn'):
			from .Nxdn import Nxdn
			self._nxdn = Nxdn(self._core, self._cmd_group)
		return self._nxdn

	@property
	def ptFive(self):
		"""ptFive commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_ptFive'):
			from .PtFive import PtFive
			self._ptFive = PtFive(self._core, self._cmd_group)
		return self._ptFive

	@property
	def tetra(self):
		"""tetra commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_tetra'):
			from .Tetra import Tetra
			self._tetra = Tetra(self._core, self._cmd_group)
		return self._tetra

	@property
	def custom(self):
		"""custom commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_custom'):
			from .Custom import Custom
			self._custom = Custom(self._core, self._cmd_group)
		return self._custom

	@property
	def limit(self):
		"""limit commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import Limit
			self._limit = Limit(self._core, self._cmd_group)
		return self._limit

	@property
	def iqRecorder(self):
		"""iqRecorder commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_iqRecorder'):
			from .IqRecorder import IqRecorder
			self._iqRecorder = IqRecorder(self._core, self._cmd_group)
		return self._iqRecorder

	@property
	def result(self):
		"""result commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_result'):
			from .Result import Result
			self._result = Result(self._core, self._cmd_group)
		return self._result

	def get_crepetition(self) -> bool:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:CREPetition \n
		Snippet: value: bool = driver.configure.vse.measurement.get_crepetition() \n
		Enables or disables the automatic configuration of the repetition mode. With enabled automatic configuration, the
		repetition mode of all measurements is set to 'Continuous' each time the instrument switches from remote operation to
		manual operation. \n
			:return: continuous_repetition: No help available
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:CREPetition?')
		return Conversions.str_to_bool(response)

	def set_crepetition(self, continuous_repetition: bool) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:CREPetition \n
		Snippet: driver.configure.vse.measurement.set_crepetition(continuous_repetition = False) \n
		Enables or disables the automatic configuration of the repetition mode. With enabled automatic configuration, the
		repetition mode of all measurements is set to 'Continuous' each time the instrument switches from remote operation to
		manual operation. \n
			:param continuous_repetition: OFF | ON
		"""
		param = Conversions.bool_to_str(continuous_repetition)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:CREPetition {param}')

	def get_scount(self) -> int:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:SCOunt \n
		Snippet: value: int = driver.configure.vse.measurement.get_scount() \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval delivers a single 'Current'
		value per result. \n
			:return: statistic_count: Range: 1 to 1000
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:SCOunt \n
		Snippet: driver.configure.vse.measurement.set_scount(statistic_count = 1) \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval delivers a single 'Current'
		value per result. \n
			:param statistic_count: Range: 1 to 1000
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:SCOunt {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.vse.measurement.get_repetition() \n
		Selects whether the measurement is repeated continuously or not. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after the statistic count CONTinuous Continuous measurement, running until explicitly terminated
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:REPetition \n
		Snippet: driver.configure.vse.measurement.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Selects whether the measurement is repeated continuously or not. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after the statistic count CONTinuous Continuous measurement, running until explicitly terminated
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:REPetition {param}')

	# noinspection PyTypeChecker
	def get_scondition(self) -> enums.StopCondition:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:SCONdition \n
		Snippet: value: enums.StopCondition = driver.configure.vse.measurement.get_scondition() \n
		No command help available \n
			:return: stop_condition: No help available
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:SCONdition?')
		return Conversions.str_to_scalar_enum(response, enums.StopCondition)

	def set_scondition(self, stop_condition: enums.StopCondition) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:SCONdition \n
		Snippet: driver.configure.vse.measurement.set_scondition(stop_condition = enums.StopCondition.NONE) \n
		No command help available \n
			:param stop_condition: No help available
		"""
		param = Conversions.enum_scalar_to_str(stop_condition, enums.StopCondition)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:SCONdition {param}')

	def get_rcoupling(self) -> bool:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:RCOupling \n
		Snippet: value: bool = driver.configure.vse.measurement.get_rcoupling() \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:return: repetition_coupling: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:RCOupling?')
		return Conversions.str_to_bool(response)

	def set_rcoupling(self, repetition_coupling: bool) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:RCOupling \n
		Snippet: driver.configure.vse.measurement.set_rcoupling(repetition_coupling = False) \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:param repetition_coupling: OFF | ON
		"""
		param = Conversions.bool_to_str(repetition_coupling)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:RCOupling {param}')

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:TOUT \n
		Snippet: value: float = driver.configure.vse.measurement.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: tcd_timeout: No help available
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_timeout: float) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:TOUT \n
		Snippet: driver.configure.vse.measurement.set_timeout(tcd_timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param tcd_timeout: No help available
		"""
		param = Conversions.decimal_value_to_str(tcd_timeout)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:TOUT {param}')

	# noinspection PyTypeChecker
	def get_standard(self) -> enums.Standard:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:STANdard \n
		Snippet: value: enums.Standard = driver.configure.vse.measurement.get_standard() \n
		Selects the digital standard of the measured signal. \n
			:return: standard: DMR | DPMR | NXDN | P25 | TETRa | LTE | SPECtrum | CUSTom
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.Standard)

	def set_standard(self, standard: enums.Standard) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:STANdard \n
		Snippet: driver.configure.vse.measurement.set_standard(standard = enums.Standard.CUSTom) \n
		Selects the digital standard of the measured signal. \n
			:param standard: DMR | DPMR | NXDN | P25 | TETRa | LTE | SPECtrum | CUSTom
		"""
		param = Conversions.enum_scalar_to_str(standard, enums.Standard)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:STANdard {param}')

	def clone(self) -> 'Measurement':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Measurement(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
