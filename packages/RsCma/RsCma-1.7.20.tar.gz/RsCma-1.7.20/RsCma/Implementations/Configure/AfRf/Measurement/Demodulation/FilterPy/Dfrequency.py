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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DFRequency \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.dfrequency.set(distor_freq_left = 1.0, distor_freq_right = 1.0) \n
		Configures the reference frequency for single-tone measurements via the RF input path. For FM stereo, the settings
		configure the left and the right audio channel. For other modulation types, only <DistorFreqLeft> is relevant.
		<DistorFreqRight> has no effect. \n
			:param distor_freq_left: Range: 0 Hz to 10.5 kHz, Unit: Hz
			:param distor_freq_right: Range: 0 Hz to 10.5 kHz, Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('distor_freq_left', distor_freq_left, DataType.Float), ArgSingle('distor_freq_right', distor_freq_right, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DFRequency {param}'.rstrip())

	# noinspection PyTypeChecker
	class DfrequencyStruct(StructBase):
		"""Response structure. Fields: \n
			- Distor_Freq_Left: float: Range: 0 Hz to 10.5 kHz, Unit: Hz
			- Distor_Freq_Right: float: Range: 0 Hz to 10.5 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Distor_Freq_Left'),
			ArgStruct.scalar_float('Distor_Freq_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Distor_Freq_Left: float = None
			self.Distor_Freq_Right: float = None

	def get(self) -> DfrequencyStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DFRequency \n
		Snippet: value: DfrequencyStruct = driver.configure.afRf.measurement.demodulation.filterPy.dfrequency.get() \n
		Configures the reference frequency for single-tone measurements via the RF input path. For FM stereo, the settings
		configure the left and the right audio channel. For other modulation types, only <DistorFreqLeft> is relevant.
		<DistorFreqRight> has no effect. \n
			:return: structure: for return value, see the help for DfrequencyStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DFRequency?', self.__class__.DfrequencyStruct())
