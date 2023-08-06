from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	def set(self, left_user_val: float, right_user_val: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:USER \n
		Snippet: driver.configure.afRf.measurement.spdif.level.peak.delta.user.set(left_user_val = 1.0, right_user_val = 1.0) \n
		For level peak, configures the AF signal user reference value of SPDIF path. \n
			:param left_user_val: Unit: %
			:param right_user_val: Unit: %
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('left_user_val', left_user_val, DataType.Float), ArgSingle('right_user_val', right_user_val, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:USER {param}'.rstrip())

	# noinspection PyTypeChecker
	class UserStruct(StructBase):
		"""Response structure. Fields: \n
			- Left_User_Val: float: Unit: %
			- Right_User_Val: float: Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_float('Left_User_Val'),
			ArgStruct.scalar_float('Right_User_Val')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Left_User_Val: float = None
			self.Right_User_Val: float = None

	def get(self) -> UserStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:USER \n
		Snippet: value: UserStruct = driver.configure.afRf.measurement.spdif.level.peak.delta.user.get() \n
		For level peak, configures the AF signal user reference value of SPDIF path. \n
			:return: structure: for return value, see the help for UserStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:PEAK:DELTa:USER?', self.__class__.UserStruct())
