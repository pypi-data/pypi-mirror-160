from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reference:
	"""Reference commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reference", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import Frequency
			self._frequency = Frequency(self._core, self._cmd_group)
		return self._frequency

	@property
	def internal(self):
		"""internal commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_internal'):
			from .Internal import Internal
			self._internal = Internal(self._core, self._cmd_group)
		return self._internal

	@property
	def external(self):
		"""external commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_external'):
			from .External import External
			self._external = External(self._core, self._cmd_group)
		return self._external

	def clone(self) -> 'Reference':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Reference(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
