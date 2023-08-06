from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nlevel:
	"""Nlevel commands group definition. 4 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nlevel", core, parent)

	@property
	def trace(self):
		"""trace commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import Trace
			self._trace = Trace(self._core, self._cmd_group)
		return self._trace

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Lower_Noise_Level: float: Noise level at lower frequency Unit: V
			- Higher_Noise_Level: float: Noise level at higher frequency Unit: V"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Lower_Noise_Level'),
			ArgStruct.scalar_float('Higher_Noise_Level')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Lower_Noise_Level: float = None
			self.Higher_Noise_Level: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:NLEVel \n
		Snippet: value: ResultData = driver.afRf.measurement.searchRoutines.rifBandwidth.nlevel.fetch() \n
		Query the lower and higher noise level values for the RX IF bandwidth measurement. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:NLEVel?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:NLEVel \n
		Snippet: value: ResultData = driver.afRf.measurement.searchRoutines.rifBandwidth.nlevel.read() \n
		Query the lower and higher noise level values for the RX IF bandwidth measurement. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:NLEVel?', self.__class__.ResultData())

	def clone(self) -> 'Nlevel':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nlevel(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
