from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cfrequency:
	"""Cfrequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cfrequency", core, parent)

	def set(self, frequency_left: float, frequency_right: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:CFRequency \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.bpass.cfrequency.set(frequency_left = 1.0, frequency_right = 1.0) \n
		Configures the center frequency of the variable bandpass filter in the SPDIF input path. \n
			:param frequency_left: Frequency for left SPDIF channel Unit: Hz
			:param frequency_right: Frequency for right SPDIF channel Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('frequency_left', frequency_left, DataType.Float), ArgSingle('frequency_right', frequency_right, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:CFRequency {param}'.rstrip())

	# noinspection PyTypeChecker
	class CfrequencyStruct(StructBase):
		"""Response structure. Fields: \n
			- Frequency_Left: float: Frequency for left SPDIF channel Unit: Hz
			- Frequency_Right: float: Frequency for right SPDIF channel Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Frequency_Left'),
			ArgStruct.scalar_float('Frequency_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Frequency_Left: float = None
			self.Frequency_Right: float = None

	def get(self) -> CfrequencyStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:CFRequency \n
		Snippet: value: CfrequencyStruct = driver.configure.afRf.measurement.spdif.filterPy.bpass.cfrequency.get() \n
		Configures the center frequency of the variable bandpass filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for CfrequencyStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:CFRequency?', self.__class__.CfrequencyStruct())
