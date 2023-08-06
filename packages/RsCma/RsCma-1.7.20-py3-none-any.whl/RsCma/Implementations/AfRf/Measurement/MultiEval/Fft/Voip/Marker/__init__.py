from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Marker:
	"""Marker commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("marker", core, parent)
		
		self._cmd_group.multi_repcap_types = "Marker,MarkerOther"

	@property
	def absolute(self):
		"""absolute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_absolute'):
			from .Absolute import Absolute
			self._absolute = Absolute(self._core, self._cmd_group)
		return self._absolute

	@property
	def relative(self):
		"""relative commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_relative'):
			from .Relative import Relative
			self._relative = Relative(self._core, self._cmd_group)
		return self._relative

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Xvalue: float: X-value of the marker Unit: Hz
			- Absolute_Yvalue: float: Y-value of the marker Unit: Depends on input path and demodulation type"""
		__meta_args_list = [
			ArgStruct.scalar_float('Xvalue'),
			ArgStruct.scalar_float('Absolute_Yvalue')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Xvalue: float = None
			self.Absolute_Yvalue: float = None

	def fetch(self, trace: enums.Statistic, freq_value: float, marker=repcap.Marker.Nr1) -> FetchStruct:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:FFT:VOIP:MARKer<mnr> \n
		Snippet: value: FetchStruct = driver.afRf.measurement.multiEval.fft.voip.marker.fetch(trace = enums.Statistic.AVERage, freq_value = 1.0, marker = repcap.Marker.Nr1) \n
		Move marker number <mnr> to a specified x-value and return the absolute coordinates. Absolute placement is used. Select
		the trace to be evaluated and the x-value. \n
			:param trace: CURRent | AVERage | MAXimum | MINimum Selects the trace type
			:param freq_value: X-value for which the coordinates are queried Range: 0 Hz to 21 kHz
			:param marker: optional repeated capability selector. Default value: Nr1
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('trace', trace, DataType.Enum, enums.Statistic), ArgSingle('freq_value', freq_value, DataType.Float))
		marker_cmd_val = self._cmd_group.get_repcap_cmd_value(marker, repcap.Marker)
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:FFT:VOIP:MARKer{marker_cmd_val}? {param}'.rstrip(), self.__class__.FetchStruct())

	def clone(self) -> 'Marker':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Marker(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
