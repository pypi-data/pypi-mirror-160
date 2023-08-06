from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Relative:
	"""Relative commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("relative", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Dx_Value: float: Delta X value of the marker relative to the reference marker Unit: Hz
			- Dy_Value: float: Delta Y value of the marker relative to the reference marker Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Dx_Value'),
			ArgStruct.scalar_float('Dy_Value')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dx_Value: float = None
			self.Dy_Value: float = None

	def fetch(self, trace: enums.Statistic, function: enums.MarkerFunction = None, markerOther=repcap.MarkerOther.Nr2) -> FetchStruct:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:MARKer<nr>:RELative \n
		Snippet: value: FetchStruct = driver.gprfMeasurement.fftSpecAn.marker.relative.fetch(trace = enums.Statistic.AVERage, function = enums.MarkerFunction.MAX, markerOther = repcap.MarkerOther.Nr2) \n
		Queries the relative coordinates of marker number <no>. Select the trace to be evaluated. Optionally, you can perform a
		marker action before reading the position. \n
			:param trace: CURRent | AVERage | MAXimum | MINimum Selects the trace type
			:param function: MIN | MAX | MAXL | MAXR | MAXN Marker action to be performed before the query MIN Search the absolute minimum of the entire trace MAX Search the absolute maximum of the entire trace MAXL Search the absolute maximum to the left of the current marker position MAXR Search the absolute maximum to the right of the current marker position MAXN Search the next lower peak of the entire trace
			:param markerOther: optional repeated capability selector. Default value: Nr2
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('trace', trace, DataType.Enum, enums.Statistic), ArgSingle('function', function, DataType.Enum, enums.MarkerFunction, is_optional=True))
		markerOther_cmd_val = self._cmd_group.get_repcap_cmd_value(markerOther, repcap.MarkerOther)
		return self._core.io.query_struct(f'FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:MARKer{markerOther_cmd_val}:RELative? {param}'.rstrip(), self.__class__.FetchStruct())
