from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CumulativeDistribFnc:
	"""CumulativeDistribFnc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cumulativeDistribFnc", core, parent)

	def set(self, lower: float, upper: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CCDF \n
		Snippet: driver.configure.gprfMeasurement.nrt.forward.limit.cumulativeDistribFnc.set(lower = 1.0, upper = 1.0) \n
		Configures limits for the CCDF results. \n
			:param lower: Range: 0 % to 100 %, Unit: %
			:param upper: Range: 0 % to 100 %, Unit: %
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('lower', lower, DataType.Float), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CCDF {param}'.rstrip())

	# noinspection PyTypeChecker
	class CumulativeDistribFncStruct(StructBase):
		"""Response structure. Fields: \n
			- Lower: float: Range: 0 % to 100 %, Unit: %
			- Upper: float: Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> CumulativeDistribFncStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CCDF \n
		Snippet: value: CumulativeDistribFncStruct = driver.configure.gprfMeasurement.nrt.forward.limit.cumulativeDistribFnc.get() \n
		Configures limits for the CCDF results. \n
			:return: structure: for return value, see the help for CumulativeDistribFncStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CCDF?', self.__class__.CumulativeDistribFncStruct())
