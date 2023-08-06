from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	def set(self, limit_lower: float, limit_upper: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:POWer \n
		Snippet: driver.configure.gprfMeasurement.acp.limit.power.set(limit_lower = 1.0, limit_upper = 1.0) \n
		Configures limits for the absolute power measured in the designated channel. \n
			:param limit_lower: Lower power limit Range: -130 dBm to 55 dBm, Unit: dBm
			:param limit_upper: Upper power limit Range: -130 dBm to 55 dBm, Unit: dBm
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('limit_lower', limit_lower, DataType.Float), ArgSingle('limit_upper', limit_upper, DataType.Float))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:POWer {param}'.rstrip())

	# noinspection PyTypeChecker
	class PowerStruct(StructBase):
		"""Response structure. Fields: \n
			- Limit_Lower: float: Lower power limit Range: -130 dBm to 55 dBm, Unit: dBm
			- Limit_Upper: float: Upper power limit Range: -130 dBm to 55 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_float('Limit_Lower'),
			ArgStruct.scalar_float('Limit_Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Limit_Lower: float = None
			self.Limit_Upper: float = None

	def get(self) -> PowerStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:POWer \n
		Snippet: value: PowerStruct = driver.configure.gprfMeasurement.acp.limit.power.get() \n
		Configures limits for the absolute power measured in the designated channel. \n
			:return: structure: for return value, see the help for PowerStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:POWer?', self.__class__.PowerStruct())
