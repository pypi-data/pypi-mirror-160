from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Timeout:
	"""Timeout commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("timeout", core, parent)

	def set(self, enable: bool, mode: enums.TimeoutMode, timeout: float = None) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOUT \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dialing.timeout.set(enable = False, mode = enums.TimeoutMode.AUTO, timeout = 1.0) \n
		No command help available \n
			:param enable: No help available
			:param mode: No help available
			:param timeout: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('mode', mode, DataType.Enum, enums.TimeoutMode), ArgSingle('timeout', timeout, DataType.Float, None, is_optional=True))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOUT {param}'.rstrip())

	# noinspection PyTypeChecker
	class TimeoutStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: No parameter help available
			- Mode: enums.TimeoutMode: No parameter help available
			- Timeout: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_enum('Mode', enums.TimeoutMode),
			ArgStruct.scalar_float('Timeout')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Mode: enums.TimeoutMode = None
			self.Timeout: float = None

	def get(self) -> TimeoutStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOUT \n
		Snippet: value: TimeoutStruct = driver.configure.afRf.measurement.multiEval.tones.dialing.timeout.get() \n
		No command help available \n
			:return: structure: for return value, see the help for TimeoutStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOUT?', self.__class__.TimeoutStruct())
