from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	def set(self, enable: bool, lower: float, upper: float) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:POWer \n
		Snippet: driver.configure.vse.measurement.limit.rfCarrier.power.set(enable = False, lower = 1.0, upper = 1.0) \n
		Configures limits for the measured RF power (PEP) . \n
			:param enable: OFF | ON Enables or disables the limit check
			:param lower: Lower power limit Range: -130 dBm to 55 dBm, Unit: dBm
			:param upper: Upper power limit Range: -130 dBm to 55 dBm, Unit: dBm
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('lower', lower, DataType.Float), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:POWer {param}'.rstrip())

	# noinspection PyTypeChecker
	class PowerStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower power limit Range: -130 dBm to 55 dBm, Unit: dBm
			- Upper: float: Upper power limit Range: -130 dBm to 55 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> PowerStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:POWer \n
		Snippet: value: PowerStruct = driver.configure.vse.measurement.limit.rfCarrier.power.get() \n
		Configures limits for the measured RF power (PEP) . \n
			:return: structure: for return value, see the help for PowerStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:VSE:MEASurement<Instance>:LIMit:RFCarrier:POWer?', self.__class__.PowerStruct())
