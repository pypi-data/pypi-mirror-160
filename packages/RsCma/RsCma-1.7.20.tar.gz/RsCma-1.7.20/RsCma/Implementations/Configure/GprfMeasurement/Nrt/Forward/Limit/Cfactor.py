from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cfactor:
	"""Cfactor commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cfactor", core, parent)

	def set(self, lower: float, upper: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CFACtor \n
		Snippet: driver.configure.gprfMeasurement.nrt.forward.limit.cfactor.set(lower = 1.0, upper = 1.0) \n
		Configures limits for the crest factor results. \n
			:param lower: Range: 0 dB to 50 dB, Unit: dB
			:param upper: Range: 0 dB to 50 dB, Unit: dB
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('lower', lower, DataType.Float), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CFACtor {param}'.rstrip())

	# noinspection PyTypeChecker
	class CfactorStruct(StructBase):
		"""Response structure. Fields: \n
			- Lower: float: Range: 0 dB to 50 dB, Unit: dB
			- Upper: float: Range: 0 dB to 50 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> CfactorStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CFACtor \n
		Snippet: value: CfactorStruct = driver.configure.gprfMeasurement.nrt.forward.limit.cfactor.get() \n
		Configures limits for the crest factor results. \n
			:return: structure: for return value, see the help for CfactorStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CFACtor?', self.__class__.CfactorStruct())
