from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Timeout:
	"""Timeout commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("timeout", core, parent)

	def set(self, enable: bool, timeout: float = None) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOUT \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dcs.timeout.set(enable = False, timeout = 1.0) \n
		Configures a timeout for completion of the first DCS measurement cycle. \n
			:param enable: OFF | ON Enables or disables the timeout
			:param timeout: Waiting for a turn-off code is aborted after this time. Range: 0.1 s to 15 s, Unit: s
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('timeout', timeout, DataType.Float, None, is_optional=True))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOUT {param}'.rstrip())

	# noinspection PyTypeChecker
	class TimeoutStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the timeout
			- Timeout: float: Waiting for a turn-off code is aborted after this time. Range: 0.1 s to 15 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Timeout')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Timeout: float = None

	def get(self) -> TimeoutStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOUT \n
		Snippet: value: TimeoutStruct = driver.configure.afRf.measurement.multiEval.tones.dcs.timeout.get() \n
		Configures a timeout for completion of the first DCS measurement cycle. \n
			:return: structure: for return value, see the help for TimeoutStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOUT?', self.__class__.TimeoutStruct())
