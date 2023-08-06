from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Range:
	"""Range commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("range", core, parent)

	def set(self, range_py: enums.ArbSamplesRange, start: int = None, stop: int = None) -> None:
		"""SCPI: SOURce:XRT:GENerator<Instance>:ARB:SAMPles:RANGe \n
		Snippet: driver.source.xrt.generator.arb.samples.range.set(range_py = enums.ArbSamplesRange.FULL, start = 1, stop = 1) \n
		Selects whether all samples or a subrange of samples is processed. \n
			:param range_py: FULL | SUB FULL Process all samples SUB Process a subrange according to Start and Stop.
			:param start: Start of the subrange (always first sample, labeled zero) Range: 0 (fixed value)
			:param stop: End of the subrange Range: 16 to samples in ARB file - 1
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('range_py', range_py, DataType.Enum, enums.ArbSamplesRange), ArgSingle('start', start, DataType.Integer, None, is_optional=True), ArgSingle('stop', stop, DataType.Integer, None, is_optional=True))
		self._core.io.write(f'SOURce:XRT:GENerator<Instance>:ARB:SAMPles:RANGe {param}'.rstrip())

	# noinspection PyTypeChecker
	class RangeStruct(StructBase):
		"""Response structure. Fields: \n
			- Range_Py: enums.ArbSamplesRange: FULL | SUB FULL Process all samples SUB Process a subrange according to Start and Stop.
			- Start: int: Start of the subrange (always first sample, labeled zero) Range: 0 (fixed value)
			- Stop: int: End of the subrange Range: 16 to samples in ARB file - 1"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Range_Py', enums.ArbSamplesRange),
			ArgStruct.scalar_int('Start'),
			ArgStruct.scalar_int('Stop')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Range_Py: enums.ArbSamplesRange = None
			self.Start: int = None
			self.Stop: int = None

	def get(self) -> RangeStruct:
		"""SCPI: SOURce:XRT:GENerator<Instance>:ARB:SAMPles:RANGe \n
		Snippet: value: RangeStruct = driver.source.xrt.generator.arb.samples.range.get() \n
		Selects whether all samples or a subrange of samples is processed. \n
			:return: structure: for return value, see the help for RangeStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:XRT:GENerator<Instance>:ARB:SAMPles:RANGe?', self.__class__.RangeStruct())
