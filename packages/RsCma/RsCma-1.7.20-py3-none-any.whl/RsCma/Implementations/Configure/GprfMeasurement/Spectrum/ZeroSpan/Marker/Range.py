from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Range:
	"""Range commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("range", core, parent)

	def set(self, xrange_lower: float, xrange_upper: float, marker=repcap.Marker.Nr1) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer<nr>:RANGe \n
		Snippet: driver.configure.gprfMeasurement.spectrum.zeroSpan.marker.range.set(xrange_lower = 1.0, xrange_upper = 1.0, marker = repcap.Marker.Nr1) \n
		Specifies the peak search range, for marker number <no> and zero span mode. Marker number one is the reference marker. \n
			:param xrange_lower: Range: 0 s to SweepTime, Unit: s
			:param xrange_upper: Range: 0 s to SweepTime, Unit: s
			:param marker: optional repeated capability selector. Default value: Nr1
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('xrange_lower', xrange_lower, DataType.Float), ArgSingle('xrange_upper', xrange_upper, DataType.Float))
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer{marker_cmd_val}:RANGe {param}'.rstrip())

	# noinspection PyTypeChecker
	class RangeStruct(StructBase):
		"""Response structure. Fields: \n
			- Xrange_Lower: float: Range: 0 s to SweepTime, Unit: s
			- Xrange_Upper: float: Range: 0 s to SweepTime, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_float('Xrange_Lower'),
			ArgStruct.scalar_float('Xrange_Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Xrange_Lower: float = None
			self.Xrange_Upper: float = None

	def get(self, marker=repcap.Marker.Nr1) -> RangeStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer<nr>:RANGe \n
		Snippet: value: RangeStruct = driver.configure.gprfMeasurement.spectrum.zeroSpan.marker.range.get(marker = repcap.Marker.Nr1) \n
		Specifies the peak search range, for marker number <no> and zero span mode. Marker number one is the reference marker. \n
			:param marker: optional repeated capability selector. Default value: Nr1
			:return: structure: for return value, see the help for RangeStruct structure arguments."""
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer{marker_cmd_val}:RANGe?', self.__class__.RangeStruct())
