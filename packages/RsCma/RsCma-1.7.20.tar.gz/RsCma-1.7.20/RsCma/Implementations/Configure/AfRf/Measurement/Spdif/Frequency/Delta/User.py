from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	def set(self, left_val: float, right_val: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FREQuency:DELTa:USER \n
		Snippet: driver.configure.afRf.measurement.spdif.frequency.delta.user.set(left_val = 1.0, right_val = 1.0) \n
		Configures the AF frequency user reference value for SPDIF path. \n
			:param left_val: Unit: Hz
			:param right_val: Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('left_val', left_val, DataType.Float), ArgSingle('right_val', right_val, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FREQuency:DELTa:USER {param}'.rstrip())

	# noinspection PyTypeChecker
	class UserStruct(StructBase):
		"""Response structure. Fields: \n
			- Left_Val: float: Unit: Hz
			- Right_Val: float: Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Left_Val'),
			ArgStruct.scalar_float('Right_Val')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Left_Val: float = None
			self.Right_Val: float = None

	def get(self) -> UserStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FREQuency:DELTa:USER \n
		Snippet: value: UserStruct = driver.configure.afRf.measurement.spdif.frequency.delta.user.get() \n
		Configures the AF frequency user reference value for SPDIF path. \n
			:return: structure: for return value, see the help for UserStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FREQuency:DELTa:USER?', self.__class__.UserStruct())
