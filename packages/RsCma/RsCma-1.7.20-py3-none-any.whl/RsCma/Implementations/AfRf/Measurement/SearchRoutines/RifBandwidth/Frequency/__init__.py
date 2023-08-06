from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 4 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

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
			- Lower_Freq: float: Lower RF frequency Unit: Hz
			- Higher_Freq: float: Higher RF frequency Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Lower_Freq'),
			ArgStruct.scalar_float('Higher_Freq')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Lower_Freq: float = None
			self.Higher_Freq: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:FREQuency \n
		Snippet: value: ResultData = driver.afRf.measurement.searchRoutines.rifBandwidth.frequency.fetch() \n
		Query the lower and higher RF frequencies left and right from the nominal frequency. At the frequency values, the noise
		has increased to the noise target value (noise level method) . Or, the SINAD audio signal quality has dropped down to the
		target value (TIA-603-D method) . \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:FREQuency?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:FREQuency \n
		Snippet: value: ResultData = driver.afRf.measurement.searchRoutines.rifBandwidth.frequency.read() \n
		Query the lower and higher RF frequencies left and right from the nominal frequency. At the frequency values, the noise
		has increased to the noise target value (noise level method) . Or, the SINAD audio signal quality has dropped down to the
		target value (TIA-603-D method) . \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:FREQuency?', self.__class__.ResultData())

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
