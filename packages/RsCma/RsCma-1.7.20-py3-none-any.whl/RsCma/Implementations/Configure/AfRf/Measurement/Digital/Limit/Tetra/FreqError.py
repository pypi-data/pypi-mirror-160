from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FreqError:
	"""FreqError commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("freqError", core, parent)

	def set(self, enable_limit: bool, upper: float, lower: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:LIMit:TETRa:FERRor \n
		Snippet: driver.configure.afRf.measurement.digital.limit.tetra.freqError.set(enable_limit = False, upper = 1.0, lower = 1.0) \n
		Enables a limit check and sets the lower and upper limits for the frequency error. \n
			:param enable_limit: OFF | ON
			:param upper: Range: -130 dBm to 55 dBm, Unit: Hz
			:param lower: Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable_limit', enable_limit, DataType.Boolean), ArgSingle('upper', upper, DataType.Float), ArgSingle('lower', lower, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:LIMit:TETRa:FERRor {param}'.rstrip())

	# noinspection PyTypeChecker
	class FreqErrorStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable_Limit: bool: OFF | ON
			- Upper: float: Range: -130 dBm to 55 dBm, Unit: Hz
			- Lower: float: Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Limit'),
			ArgStruct.scalar_float('Upper'),
			ArgStruct.scalar_float('Lower')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Limit: bool = None
			self.Upper: float = None
			self.Lower: float = None

	def get(self) -> FreqErrorStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:LIMit:TETRa:FERRor \n
		Snippet: value: FreqErrorStruct = driver.configure.afRf.measurement.digital.limit.tetra.freqError.get() \n
		Enables a limit check and sets the lower and upper limits for the frequency error. \n
			:return: structure: for return value, see the help for FreqErrorStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:LIMit:TETRa:FERRor?', self.__class__.FreqErrorStruct())
