from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Condition:
	"""Condition commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("condition", core, parent)

	@property
	def off(self):
		"""off commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_off'):
			from .Off import Off
			self._off = Off(self._core, self._cmd_group)
		return self._off

	@property
	def pending(self):
		"""pending commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pending'):
			from .Pending import Pending
			self._pending = Pending(self._core, self._cmd_group)
		return self._pending

	@property
	def on(self):
		"""on commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_on'):
			from .On import On
			self._on = On(self._core, self._cmd_group)
		return self._on

	def clone(self) -> 'Condition':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Condition(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
