from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Level:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def set(self, level_left: float, level_right: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT:LEVel \n
		Snippet: driver.source.afRf.generator.sout.level.set(level_left = 1.0, level_right = 1.0) \n
		Specifies the output levels for the SPDIF OUT connector. For noise signals provided by an internal generator, the maximum
		allowed level is reduced by the factor 1/sqrt(2) . \n
			:param level_left: Level for the left channel Range: 0.01 % to 100 %, Unit: %
			:param level_right: Level for the right channel Range: 0.01 % to 100 %, Unit: %
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('level_left', level_left, DataType.Float), ArgSingle('level_right', level_right, DataType.Float))
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:SOUT:LEVel {param}'.rstrip())

	# noinspection PyTypeChecker
	class LevelStruct(StructBase):
		"""Response structure. Fields: \n
			- Level_Left: float: Level for the left channel Range: 0.01 % to 100 %, Unit: %
			- Level_Right: float: Level for the right channel Range: 0.01 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_float('Level_Left'),
			ArgStruct.scalar_float('Level_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Level_Left: float = None
			self.Level_Right: float = None

	def get(self) -> LevelStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT:LEVel \n
		Snippet: value: LevelStruct = driver.source.afRf.generator.sout.level.get() \n
		Specifies the output levels for the SPDIF OUT connector. For noise signals provided by an internal generator, the maximum
		allowed level is reduced by the factor 1/sqrt(2) . \n
			:return: structure: for return value, see the help for LevelStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:AFRF:GENerator<Instance>:SOUT:LEVel?', self.__class__.LevelStruct())
