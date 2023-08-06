from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dfrequency:
	"""Dfrequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dfrequency", core, parent)

	def set(self, distor_freq_left: float, distor_freq_right: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DFRequency \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.dfrequency.set(distor_freq_left = 1.0, distor_freq_right = 1.0) \n
		Configures the reference frequency for single-tone measurements via the SPDIF input path. \n
			:param distor_freq_left: Frequency for left SPDIF channel Unit: Hz
			:param distor_freq_right: Frequency for right SPDIF channel Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('distor_freq_left', distor_freq_left, DataType.Float), ArgSingle('distor_freq_right', distor_freq_right, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DFRequency {param}'.rstrip())

	# noinspection PyTypeChecker
	class DfrequencyStruct(StructBase):
		"""Response structure. Fields: \n
			- Distor_Freq_Left: float: Frequency for left SPDIF channel Unit: Hz
			- Distor_Freq_Right: float: Frequency for right SPDIF channel Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Distor_Freq_Left'),
			ArgStruct.scalar_float('Distor_Freq_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Distor_Freq_Left: float = None
			self.Distor_Freq_Right: float = None

	def get(self) -> DfrequencyStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DFRequency \n
		Snippet: value: DfrequencyStruct = driver.configure.afRf.measurement.spdif.filterPy.dfrequency.get() \n
		Configures the reference frequency for single-tone measurements via the SPDIF input path. \n
			:return: structure: for return value, see the help for DfrequencyStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:DFRequency?', self.__class__.DfrequencyStruct())
