from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pep:
	"""Pep commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pep", core, parent)

	def set(self, lower: float, upper: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:PEP \n
		Snippet: driver.configure.gprfMeasurement.nrt.forward.limit.pep.set(lower = 1.0, upper = 1.0) \n
		Configures limits for the PEP results. \n
			:param lower: Range: Depends on sensor model , Unit: dBm
			:param upper: Range: Depends on sensor model , Unit: dBm
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('lower', lower, DataType.Float), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:PEP {param}'.rstrip())

	# noinspection PyTypeChecker
	class PepStruct(StructBase):
		"""Response structure. Fields: \n
			- Lower: float: Range: Depends on sensor model , Unit: dBm
			- Upper: float: Range: Depends on sensor model , Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> PepStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:PEP \n
		Snippet: value: PepStruct = driver.configure.gprfMeasurement.nrt.forward.limit.pep.get() \n
		Configures limits for the PEP results. \n
			:return: structure: for return value, see the help for PepStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:PEP?', self.__class__.PepStruct())
