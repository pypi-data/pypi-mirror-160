from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioOutput:
	"""AudioOutput commands group definition. 6 total commands, 5 Subgroups, 1 group commands
	Repeated Capability: AudioOutput, default value after init: AudioOutput.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("audioOutput", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_audioOutput_get', 'repcap_audioOutput_set', repcap.AudioOutput.Nr1)

	def repcap_audioOutput_set(self, audioOutput: repcap.AudioOutput) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to AudioOutput.Default
		Default value after init: AudioOutput.Nr1"""
		self._cmd_group.set_repcap_enum_value(audioOutput)

	def repcap_audioOutput_get(self) -> repcap.AudioOutput:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import Delay
			self._delay = Delay(self._core, self._cmd_group)
		return self._delay

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Level import Level
			self._level = Level(self._core, self._cmd_group)
		return self._level

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import Enable
			self._enable = Enable(self._core, self._cmd_group)
		return self._enable

	@property
	def first(self):
		"""first commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_first'):
			from .First import First
			self._first = First(self._core, self._cmd_group)
		return self._first

	@property
	def second(self):
		"""second commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_second'):
			from .Second import Second
			self._second = Second(self._core, self._cmd_group)
		return self._second

	def set(self, af_out_source: enums.SignalSource, audioOutput=repcap.AudioOutput.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AOUT<nr> \n
		Snippet: driver.source.afRf.generator.audioOutput.set(af_out_source = enums.SignalSource.AFI1, audioOutput = repcap.AudioOutput.Default) \n
		Selects an audio signal source for an AF OUT connector. \n
			:param af_out_source: GEN1 | GEN2 | AFI1 | AFI2 | SPIL | SPIR GEN1 AF1 OUT source: Audio generator 1 AFI1 AF1 OUT source: AF1 IN SPIL AF1 OUT source: SPDIF IN, left channel GEN2 AF2 OUT source: Audio generator 2 AFI2 AF2 OUT source: AF2 IN SPIR AF2 OUT source: SPDIF IN, right channel
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
		"""
		param = Conversions.enum_scalar_to_str(af_out_source, enums.SignalSource)
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:AOUT{audioOutput_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, audioOutput=repcap.AudioOutput.Default) -> enums.SignalSource:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AOUT<nr> \n
		Snippet: value: enums.SignalSource = driver.source.afRf.generator.audioOutput.get(audioOutput = repcap.AudioOutput.Default) \n
		Selects an audio signal source for an AF OUT connector. \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:return: af_out_source: GEN1 | GEN2 | AFI1 | AFI2 | SPIL | SPIR GEN1 AF1 OUT source: Audio generator 1 AFI1 AF1 OUT source: AF1 IN SPIL AF1 OUT source: SPDIF IN, left channel GEN2 AF2 OUT source: Audio generator 2 AFI2 AF2 OUT source: AF2 IN SPIR AF2 OUT source: SPDIF IN, right channel"""
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:AOUT{audioOutput_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSource)

	def clone(self) -> 'AudioOutput':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AudioOutput(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
