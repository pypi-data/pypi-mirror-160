from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BitErrorRate:
	"""BitErrorRate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bitErrorRate", core, parent)

	def set(self, enable_limit: bool, upper: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:LIMit:TTL:BERate \n
		Snippet: driver.configure.afRf.measurement.digital.limit.ttl.bitErrorRate.set(enable_limit = False, upper = 1.0) \n
		Enables a limit check and sets the lower and upper limits of the bit error rate for the TTL path. \n
			:param enable_limit: OFF | ON Range: 0 % to 100 %
			:param upper: Range: -130 dBm to 55 dBm, Unit: %
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable_limit', enable_limit, DataType.Boolean), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:LIMit:TTL:BERate {param}'.rstrip())

	# noinspection PyTypeChecker
	class BitErrorRateStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable_Limit: bool: OFF | ON Range: 0 % to 100 %
			- Upper: float: Range: -130 dBm to 55 dBm, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Limit'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Limit: bool = None
			self.Upper: float = None

	def get(self) -> BitErrorRateStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:LIMit:TTL:BERate \n
		Snippet: value: BitErrorRateStruct = driver.configure.afRf.measurement.digital.limit.ttl.bitErrorRate.get() \n
		Enables a limit check and sets the lower and upper limits of the bit error rate for the TTL path. \n
			:return: structure: for return value, see the help for BitErrorRateStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:LIMit:TTL:BERate?', self.__class__.BitErrorRateStruct())
