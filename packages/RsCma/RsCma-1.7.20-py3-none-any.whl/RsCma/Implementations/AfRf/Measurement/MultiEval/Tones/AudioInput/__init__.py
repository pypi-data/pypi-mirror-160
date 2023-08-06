from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioInput:
	"""AudioInput commands group definition. 6 total commands, 2 Subgroups, 2 group commands
	Repeated Capability: AudioInput, default value after init: AudioInput.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("audioInput", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_audioInput_get', 'repcap_audioInput_set', repcap.AudioInput.Nr1)

	def repcap_audioInput_set(self, audioInput: repcap.AudioInput) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AudioInput.Default
		Default value after init: AudioInput.Nr1"""
		self._cmd_group.set_repcap_enum_value(audioInput)

	def repcap_audioInput_get(self) -> repcap.AudioInput:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def sequence(self):
		"""sequence commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sequence'):
			from .Sequence import Sequence
			self._sequence = Sequence(self._core, self._cmd_group)
		return self._sequence

	@property
	def repetitions(self):
		"""repetitions commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_repetitions'):
			from .Repetitions import Repetitions
			self._repetitions = Repetitions(self._core, self._cmd_group)
		return self._repetitions

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Length: int: Length of the tone sequence (number of digits)
			- Sequence: List[str]: Dialed digit as string
			- Frequency_1: List[float]: Nominal tone frequency according to the tone table Unit: Hz
			- Deviation_1: List[float]: Deviation of the measured tone frequency from the nominal tone frequency Unit: Hz
			- Fequency_2: List[float]: Second nominal frequency (only relevant for dual tones) Unit: Hz
			- Deviation_2: List[float]: Deviation of the second frequency (only relevant for dual tones) Unit: Hz
			- Time: List[float]: Measured tone duration Unit: s
			- Pause: List[float]: Duration of the pause between this tone and the next tone of the sequence Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Length'),
			ArgStruct('Sequence', DataType.StringList, None, False, True, 1),
			ArgStruct('Frequency_1', DataType.FloatList, None, False, True, 1),
			ArgStruct('Deviation_1', DataType.FloatList, None, False, True, 1),
			ArgStruct('Fequency_2', DataType.FloatList, None, False, True, 1),
			ArgStruct('Deviation_2', DataType.FloatList, None, False, True, 1),
			ArgStruct('Time', DataType.FloatList, None, False, True, 1),
			ArgStruct('Pause', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Length: int = None
			self.Sequence: List[str] = None
			self.Frequency_1: List[float] = None
			self.Deviation_1: List[float] = None
			self.Fequency_2: List[float] = None
			self.Deviation_2: List[float] = None
			self.Time: List[float] = None
			self.Pause: List[float] = None

	def fetch(self, audioInput=repcap.AudioInput.Default) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN<Nr> \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.tones.audioInput.fetch(audioInput = repcap.AudioInput.Default) \n
		Query all results of a tone sequence analysis. For each tone, a sequence of results is returned: <Reliability>, <Length>{,
		<Sequence>, <Frequency1>, <Deviation1>, <Frequency2>, <Deviation2>, <Time>, <Pause>}Tone 1, {...}Tone 2, ..., {...}Tone
		<Length> \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN{audioInput_cmd_val}?', self.__class__.ResultData())

	def read(self, audioInput=repcap.AudioInput.Default) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN<Nr> \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.tones.audioInput.read(audioInput = repcap.AudioInput.Default) \n
		Query all results of a tone sequence analysis. For each tone, a sequence of results is returned: <Reliability>, <Length>{,
		<Sequence>, <Frequency1>, <Deviation1>, <Frequency2>, <Deviation2>, <Time>, <Pause>}Tone 1, {...}Tone 2, ..., {...}Tone
		<Length> \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN{audioInput_cmd_val}?', self.__class__.ResultData())

	def clone(self) -> 'AudioInput':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AudioInput(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
