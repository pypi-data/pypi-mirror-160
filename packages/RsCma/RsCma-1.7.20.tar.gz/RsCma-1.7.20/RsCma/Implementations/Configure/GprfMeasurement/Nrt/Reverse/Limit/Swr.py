from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Swr:
	"""Swr commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("swr", core, parent)

	def set(self, lower: float, upper: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:SWR \n
		Snippet: driver.configure.gprfMeasurement.nrt.reverse.limit.swr.set(lower = 1.0, upper = 1.0) \n
		Configures limits for the SWR results. \n
			:param lower: Range: 1 to 50
			:param upper: Range: 1 to 50
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('lower', lower, DataType.Float), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:SWR {param}'.rstrip())

	# noinspection PyTypeChecker
	class SwrStruct(StructBase):
		"""Response structure. Fields: \n
			- Lower: float: Range: 1 to 50
			- Upper: float: Range: 1 to 50"""
		__meta_args_list = [
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> SwrStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:SWR \n
		Snippet: value: SwrStruct = driver.configure.gprfMeasurement.nrt.reverse.limit.swr.get() \n
		Configures limits for the SWR results. \n
			:return: structure: for return value, see the help for SwrStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:SWR?', self.__class__.SwrStruct())
