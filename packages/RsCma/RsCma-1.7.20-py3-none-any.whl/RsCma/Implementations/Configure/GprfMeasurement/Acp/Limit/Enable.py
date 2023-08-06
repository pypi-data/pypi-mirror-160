from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, enable_ch_0: bool, enable_ch_1: bool, enable_ch_2: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ENABle \n
		Snippet: driver.configure.gprfMeasurement.acp.limit.enable.set(enable_ch_0 = False, enable_ch_1 = False, enable_ch_2 = False) \n
		Enables or disables the ACLR and power limit checks. \n
			:param enable_ch_0: OFF | ON Absolute power limit checks for the designated channel '0'
			:param enable_ch_1: OFF | ON ACLR limit check for the neighbor channels '+1' and '-1'
			:param enable_ch_2: OFF | ON ACLR limit check for the neighbor channels '+2' and '-2'
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable_ch_0', enable_ch_0, DataType.Boolean), ArgSingle('enable_ch_1', enable_ch_1, DataType.Boolean), ArgSingle('enable_ch_2', enable_ch_2, DataType.Boolean))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ENABle {param}'.rstrip())

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable_Ch_0: bool: OFF | ON Absolute power limit checks for the designated channel '0'
			- Enable_Ch_1: bool: OFF | ON ACLR limit check for the neighbor channels '+1' and '-1'
			- Enable_Ch_2: bool: OFF | ON ACLR limit check for the neighbor channels '+2' and '-2'"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Ch_0'),
			ArgStruct.scalar_bool('Enable_Ch_1'),
			ArgStruct.scalar_bool('Enable_Ch_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Ch_0: bool = None
			self.Enable_Ch_1: bool = None
			self.Enable_Ch_2: bool = None

	def get(self) -> EnableStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ENABle \n
		Snippet: value: EnableStruct = driver.configure.gprfMeasurement.acp.limit.enable.get() \n
		Enables or disables the ACLR and power limit checks. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ENABle?', self.__class__.EnableStruct())
