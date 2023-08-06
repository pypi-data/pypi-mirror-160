from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.RepeatedCapability import RepeatedCapability
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioInput:
	"""AudioInput commands group definition. 5 total commands, 5 Subgroups, 0 group commands
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
	def mlevel(self):
		"""mlevel commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mlevel'):
			from .Mlevel import Mlevel
			self._mlevel = Mlevel(self._core, self._cmd_group)
		return self._mlevel

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

	@property
	def aranging(self):
		"""aranging commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aranging'):
			from .Aranging import Aranging
			self._aranging = Aranging(self._core, self._cmd_group)
		return self._aranging

	@property
	def icoupling(self):
		"""icoupling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icoupling'):
			from .Icoupling import Icoupling
			self._icoupling = Icoupling(self._core, self._cmd_group)
		return self._icoupling

	def clone(self) -> 'AudioInput':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AudioInput(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
