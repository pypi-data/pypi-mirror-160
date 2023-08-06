from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, power: bool, pep: bool, crest_factor: bool, ccdf: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:ENABle \n
		Snippet: driver.configure.gprfMeasurement.nrt.forward.limit.enable.set(power = False, pep = False, crest_factor = False, ccdf = False) \n
		Enables/disables the limit check for the forward direction results. \n
			:param power: OFF | ON
			:param pep: OFF | ON
			:param crest_factor: OFF | ON
			:param ccdf: OFF | ON
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('power', power, DataType.Boolean), ArgSingle('pep', pep, DataType.Boolean), ArgSingle('crest_factor', crest_factor, DataType.Boolean), ArgSingle('ccdf', ccdf, DataType.Boolean))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:ENABle {param}'.rstrip())

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Response structure. Fields: \n
			- Power: bool: OFF | ON
			- Pep: bool: OFF | ON
			- Crest_Factor: bool: OFF | ON
			- Ccdf: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Power'),
			ArgStruct.scalar_bool('Pep'),
			ArgStruct.scalar_bool('Crest_Factor'),
			ArgStruct.scalar_bool('Ccdf')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Power: bool = None
			self.Pep: bool = None
			self.Crest_Factor: bool = None
			self.Ccdf: bool = None

	def get(self) -> EnableStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:ENABle \n
		Snippet: value: EnableStruct = driver.configure.gprfMeasurement.nrt.forward.limit.enable.get() \n
		Enables/disables the limit check for the forward direction results. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:ENABle?', self.__class__.EnableStruct())
