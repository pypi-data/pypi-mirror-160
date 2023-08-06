from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BwDisplace:
	"""BwDisplace commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bwDisplace", core, parent)

	def set(self, enable: bool, lower: float = None, upper: float = None) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:BWDisplace \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.rifBandwidth.bwDisplace.set(enable = False, lower = 1.0, upper = 1.0) \n
		Enables a limit check and sets limits for the RX bandwidth / RF signal displacement bandwidth. \n
			:param enable: OFF | ON
			:param lower: Range: 1 Hz to 100000 Hz, Unit: Hz
			:param upper: Range: 1000 Hz to 1 MHz, Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('lower', lower, DataType.Float, None, is_optional=True), ArgSingle('upper', upper, DataType.Float, None, is_optional=True))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:BWDisplace {param}'.rstrip())

	# noinspection PyTypeChecker
	class BwDisplaceStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON
			- Lower: float: Range: 1 Hz to 100000 Hz, Unit: Hz
			- Upper: float: Range: 1000 Hz to 1 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> BwDisplaceStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:BWDisplace \n
		Snippet: value: BwDisplaceStruct = driver.configure.afRf.measurement.searchRoutines.limit.rifBandwidth.bwDisplace.get() \n
		Enables a limit check and sets limits for the RX bandwidth / RF signal displacement bandwidth. \n
			:return: structure: for return value, see the help for BwDisplaceStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:BWDisplace?', self.__class__.BwDisplaceStruct())
