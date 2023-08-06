from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Level:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def set(self, enable: bool, upper: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:TSENsitivity:VOIP:LEVel \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.tsensitivity.voip.level.set(enable = False, upper = 1.0) \n
		Enable and configure the upper limit of the level of the generated AF signal. \n
			:param enable: OFF | ON Enables or disables the limit check
			:param upper: Unit: V Upper limit of the level of the generated AF signal for AF/VoIP signal path.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:TSENsitivity:VOIP:LEVel {param}'.rstrip())

	# noinspection PyTypeChecker
	class LevelStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Unit: V Upper limit of the level of the generated AF signal for AF/VoIP signal path."""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get(self) -> LevelStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:TSENsitivity:VOIP:LEVel \n
		Snippet: value: LevelStruct = driver.configure.afRf.measurement.searchRoutines.limit.tsensitivity.voip.level.get() \n
		Enable and configure the upper limit of the level of the generated AF signal. \n
			:return: structure: for return value, see the help for LevelStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:TSENsitivity:VOIP:LEVel?', self.__class__.LevelStruct())
