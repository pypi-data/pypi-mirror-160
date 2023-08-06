from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Aclr:
	"""Aclr commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("aclr", core, parent)

	def set(self, limit_ch_1: float, limit_ch_2: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ACLR \n
		Snippet: driver.configure.gprfMeasurement.acp.limit.aclr.set(limit_ch_1 = 1.0, limit_ch_2 = 1.0) \n
		Configures upper limits for the measured ACLR values. \n
			:param limit_ch_1: Upper ACLR limit for the channels '+1' and '-1' Range: -80 dB to 10 dB, Unit: dB
			:param limit_ch_2: Upper ACLR limit for the channels '+2' and '-2' Range: -80 dB to 10 dB, Unit: dB
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('limit_ch_1', limit_ch_1, DataType.Float), ArgSingle('limit_ch_2', limit_ch_2, DataType.Float))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ACLR {param}'.rstrip())

	# noinspection PyTypeChecker
	class AclrStruct(StructBase):
		"""Response structure. Fields: \n
			- Limit_Ch_1: float: Upper ACLR limit for the channels '+1' and '-1' Range: -80 dB to 10 dB, Unit: dB
			- Limit_Ch_2: float: Upper ACLR limit for the channels '+2' and '-2' Range: -80 dB to 10 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Limit_Ch_1'),
			ArgStruct.scalar_float('Limit_Ch_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Limit_Ch_1: float = None
			self.Limit_Ch_2: float = None

	def get(self) -> AclrStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ACLR \n
		Snippet: value: AclrStruct = driver.configure.gprfMeasurement.acp.limit.aclr.get() \n
		Configures upper limits for the measured ACLR values. \n
			:return: structure: for return value, see the help for AclrStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ACLR?', self.__class__.AclrStruct())
