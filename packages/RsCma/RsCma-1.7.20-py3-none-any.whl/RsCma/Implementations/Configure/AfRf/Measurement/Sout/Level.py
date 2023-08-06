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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SOUT:LEVel \n
		Snippet: driver.configure.afRf.measurement.sout.level.set(level_left = 1.0, level_right = 1.0) \n
		Specifies the output levels for the SPDIF OUT connector. \n
			:param level_left: Level for the left channel Unit: %
			:param level_right: Level for the right channel Unit: %
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('level_left', level_left, DataType.Float), ArgSingle('level_right', level_right, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SOUT:LEVel {param}'.rstrip())

	# noinspection PyTypeChecker
	class LevelStruct(StructBase):
		"""Response structure. Fields: \n
			- Level_Left: float: Level for the left channel Unit: %
			- Level_Right: float: Level for the right channel Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_float('Level_Left'),
			ArgStruct.scalar_float('Level_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Level_Left: float = None
			self.Level_Right: float = None

	def get(self) -> LevelStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SOUT:LEVel \n
		Snippet: value: LevelStruct = driver.configure.afRf.measurement.sout.level.get() \n
		Specifies the output levels for the SPDIF OUT connector. \n
			:return: structure: for return value, see the help for LevelStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SOUT:LEVel?', self.__class__.LevelStruct())
