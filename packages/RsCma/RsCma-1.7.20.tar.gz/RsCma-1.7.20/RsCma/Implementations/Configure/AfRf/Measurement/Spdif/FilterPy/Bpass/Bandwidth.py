from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandwidth:
	"""Bandwidth commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bandwidth", core, parent)

	def set(self, bandwidth_left: float, bandwidth_right: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:BWIDth \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.bpass.bandwidth.set(bandwidth_left = 1.0, bandwidth_right = 1.0) \n
		Configures the bandwidth of the variable bandpass filter in the SPDIF input path. \n
			:param bandwidth_left: Bandwidth for left SPDIF channel Unit: Hz
			:param bandwidth_right: Bandwidth for right SPDIF channel Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('bandwidth_left', bandwidth_left, DataType.Float), ArgSingle('bandwidth_right', bandwidth_right, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:BWIDth {param}'.rstrip())

	# noinspection PyTypeChecker
	class BandwidthStruct(StructBase):
		"""Response structure. Fields: \n
			- Bandwidth_Left: float: Bandwidth for left SPDIF channel Unit: Hz
			- Bandwidth_Right: float: Bandwidth for right SPDIF channel Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Bandwidth_Left'),
			ArgStruct.scalar_float('Bandwidth_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Bandwidth_Left: float = None
			self.Bandwidth_Right: float = None

	def get(self) -> BandwidthStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:BWIDth \n
		Snippet: value: BandwidthStruct = driver.configure.afRf.measurement.spdif.filterPy.bpass.bandwidth.get() \n
		Configures the bandwidth of the variable bandpass filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for BandwidthStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:BPASs:BWIDth?', self.__class__.BandwidthStruct())
