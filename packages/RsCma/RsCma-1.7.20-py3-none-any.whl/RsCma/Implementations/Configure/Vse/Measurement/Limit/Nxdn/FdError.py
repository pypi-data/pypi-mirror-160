from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FdError:
	"""FdError commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdError", core, parent)

	def set(self, enable: bool, limit: float) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:NXDN:FDERor \n
		Snippet: driver.configure.vse.measurement.limit.nxdn.fdError.set(enable = False, limit = 1.0) \n
		Configures an upper limit for the measured FSK deviation error for the digital standard 'NXDN'. \n
			:param enable: OFF | ON Enables or disables the limit check
			:param limit: Upper FSK deviation error limit Range: 0 Hz to 1 MHz, Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('limit', limit, DataType.Float))
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:LIMit:NXDN:FDERor {param}'.rstrip())

	# noinspection PyTypeChecker
	class FdErrorStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Limit: float: Upper FSK deviation error limit Range: 0 Hz to 1 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get(self) -> FdErrorStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:NXDN:FDERor \n
		Snippet: value: FdErrorStruct = driver.configure.vse.measurement.limit.nxdn.fdError.get() \n
		Configures an upper limit for the measured FSK deviation error for the digital standard 'NXDN'. \n
			:return: structure: for return value, see the help for FdErrorStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:VSE:MEASurement<Instance>:LIMit:NXDN:FDERor?', self.__class__.FdErrorStruct())
