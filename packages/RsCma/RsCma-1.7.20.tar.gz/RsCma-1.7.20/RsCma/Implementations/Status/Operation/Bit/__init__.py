from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bit:
	"""Bit commands group definition. 5 total commands, 5 Subgroups, 0 group commands
	Repeated Capability: Bit, default value after init: Bit.Nr8"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bit", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_bit_get', 'repcap_bit_set', repcap.Bit.Nr8)

	def repcap_bit_set(self, bit: repcap.Bit) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Bit.Default
		Default value after init: Bit.Nr8"""
		self._cmd_group.set_repcap_enum_value(bit)

	def repcap_bit_get(self) -> repcap.Bit:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def condition(self):
		"""condition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_condition'):
			from .Condition import Condition
			self._condition = Condition(self._core, self._cmd_group)
		return self._condition

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import Enable
			self._enable = Enable(self._core, self._cmd_group)
		return self._enable

	@property
	def event(self):
		"""event commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_event'):
			from .Event import Event
			self._event = Event(self._core, self._cmd_group)
		return self._event

	@property
	def ntransition(self):
		"""ntransition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ntransition'):
			from .Ntransition import Ntransition
			self._ntransition = Ntransition(self._core, self._cmd_group)
		return self._ntransition

	@property
	def ptransition(self):
		"""ptransition commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ptransition'):
			from .Ptransition import Ptransition
			self._ptransition = Ptransition(self._core, self._cmd_group)
		return self._ptransition

	def clone(self) -> 'Bit':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Bit(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
