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
class Absolute:
	"""Absolute commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("absolute", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Xvalue: float: X-value of the marker Unit: Hz
			- Yvalue: float: Y-value of the marker Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_float('Xvalue'),
			ArgStruct.scalar_float('Yvalue')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Xvalue: float = None
			self.Yvalue: float = None

	def fetch(self, trace: enums.Statistic, function: enums.MarkerFunction = None, marker=repcap.Marker.Nr1) -> FetchStruct:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:MARKer<nr>:ABSolute \n
		Snippet: value: FetchStruct = driver.gprfMeasurement.fftSpecAn.marker.absolute.fetch(trace = enums.Statistic.AVERage, function = enums.MarkerFunction.MAX, marker = repcap.Marker.Nr1) \n
		Queries the absolute coordinates of marker number <no>. Marker number one is the reference marker. Select the trace to be
		evaluated. Optionally, you can perform a marker action before reading the position. \n
			:param trace: CURRent | AVERage | MAXimum | MINimum Selects the trace type
			:param function: MIN | MAX | MAXL | MAXR | MAXN Marker action to be performed before the query MIN Search the absolute minimum of the entire trace MAX Search the absolute maximum of the entire trace MAXL Search the absolute maximum to the left of the current marker position MAXR Search the absolute maximum to the right of the current marker position MAXN Search the next lower peak of the entire trace
			:param marker: optional repeated capability selector. Default value: Nr1
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('trace', trace, DataType.Enum, enums.Statistic), ArgSingle('function', function, DataType.Enum, enums.MarkerFunction, is_optional=True))
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		return self._core.io.query_struct(f'FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:MARKer{marker_cmd_val}:ABSolute? {param}'.rstrip(), self.__class__.FetchStruct())
