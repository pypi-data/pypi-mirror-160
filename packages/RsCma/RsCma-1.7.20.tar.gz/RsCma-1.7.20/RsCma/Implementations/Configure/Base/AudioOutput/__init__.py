from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioOutput:
	"""AudioOutput commands group definition. 5 total commands, 5 Subgroups, 0 group commands
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
	def ecircuitry(self):
		"""ecircuitry commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ecircuitry'):
			from .Ecircuitry import Ecircuitry
			self._ecircuitry = Ecircuitry(self._core, self._cmd_group)
		return self._ecircuitry

	@property
	def zbox(self):
		"""zbox commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_zbox'):
			from .Zbox import Zbox
			self._zbox = Zbox(self._core, self._cmd_group)
		return self._zbox

	@property
	def dimpedance(self):
		"""dimpedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dimpedance'):
			from .Dimpedance import Dimpedance
			self._dimpedance = Dimpedance(self._core, self._cmd_group)
		return self._dimpedance

	@property
	def eimpedance(self):
		"""eimpedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eimpedance'):
			from .Eimpedance import Eimpedance
			self._eimpedance = Eimpedance(self._core, self._cmd_group)
		return self._eimpedance

	@property
	def limpedance(self):
		"""limpedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_limpedance'):
			from .Limpedance import Limpedance
			self._limpedance = Limpedance(self._core, self._cmd_group)
		return self._limpedance

	def clone(self) -> 'AudioOutput':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AudioOutput(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
