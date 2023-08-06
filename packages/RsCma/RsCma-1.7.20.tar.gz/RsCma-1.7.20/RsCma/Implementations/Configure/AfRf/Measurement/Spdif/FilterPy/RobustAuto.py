from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RobustAuto:
	"""RobustAuto commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("robustAuto", core, parent)

	def set(self, automatic_mode_left: bool, automatic_mode_right: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:ROBustauto \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.robustAuto.set(automatic_mode_left = False, automatic_mode_right = False) \n
		Enables or disables robust automatic mode for distortion signal filtering in the SPDIF input path. \n
			:param automatic_mode_left: OFF | ON
			:param automatic_mode_right: OFF | ON
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('automatic_mode_left', automatic_mode_left, DataType.Boolean), ArgSingle('automatic_mode_right', automatic_mode_right, DataType.Boolean))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:ROBustauto {param}'.rstrip())

	# noinspection PyTypeChecker
	class RobustAutoStruct(StructBase):
		"""Response structure. Fields: \n
			- Automatic_Mode_Left: bool: OFF | ON
			- Automatic_Mode_Right: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Automatic_Mode_Left'),
			ArgStruct.scalar_bool('Automatic_Mode_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Automatic_Mode_Left: bool = None
			self.Automatic_Mode_Right: bool = None

	def get(self) -> RobustAutoStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:ROBustauto \n
		Snippet: value: RobustAutoStruct = driver.configure.afRf.measurement.spdif.filterPy.robustAuto.get() \n
		Enables or disables robust automatic mode for distortion signal filtering in the SPDIF input path. \n
			:return: structure: for return value, see the help for RobustAutoStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:ROBustauto?', self.__class__.RobustAutoStruct())
