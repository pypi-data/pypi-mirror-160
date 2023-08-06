from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ThDistortion:
	"""ThDistortion commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("thDistortion", core, parent)

	def set(self, enable_left: bool, upper_left: float, enable_right: bool, upper_right: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDistortion \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.spdif.thDistortion.set(enable_left = False, upper_left = 1.0, enable_right = False, upper_right = 1.0) \n
		Configures limits for the THD results, measured via the SPDIF input path. \n
			:param enable_left: OFF | ON Enables or disables the limit check for the left SPDIF channel
			:param upper_left: Upper THD limit for the left SPDIF channel Range: 0 % to 100 %, Unit: %
			:param enable_right: OFF | ON Enables or disables the limit check for the right SPDIF channel
			:param upper_right: Upper THD limit for the right SPDIF channel Range: 0 % to 100 %, Unit: %
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable_left', enable_left, DataType.Boolean), ArgSingle('upper_left', upper_left, DataType.Float), ArgSingle('enable_right', enable_right, DataType.Boolean), ArgSingle('upper_right', upper_right, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDistortion {param}'.rstrip())

	# noinspection PyTypeChecker
	class ThDistortionStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable_Left: bool: OFF | ON Enables or disables the limit check for the left SPDIF channel
			- Upper_Left: float: Upper THD limit for the left SPDIF channel Range: 0 % to 100 %, Unit: %
			- Enable_Right: bool: OFF | ON Enables or disables the limit check for the right SPDIF channel
			- Upper_Right: float: Upper THD limit for the right SPDIF channel Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Upper_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Upper_Left: float = None
			self.Enable_Right: bool = None
			self.Upper_Right: float = None

	def get(self) -> ThDistortionStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDistortion \n
		Snippet: value: ThDistortionStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.thDistortion.get() \n
		Configures limits for the THD results, measured via the SPDIF input path. \n
			:return: structure: for return value, see the help for ThDistortionStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDistortion?', self.__class__.ThDistortionStruct())
