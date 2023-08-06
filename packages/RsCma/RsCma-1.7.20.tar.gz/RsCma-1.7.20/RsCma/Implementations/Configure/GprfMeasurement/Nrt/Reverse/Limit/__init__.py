from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 5 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("limit", core, parent)

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import Enable
			self._enable = Enable(self._core, self._cmd_group)
		return self._enable

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Power import Power
			self._power = Power(self._core, self._cmd_group)
		return self._power

	@property
	def rloss(self):
		"""rloss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rloss'):
			from .Rloss import Rloss
			self._rloss = Rloss(self._core, self._cmd_group)
		return self._rloss

	@property
	def reflection(self):
		"""reflection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reflection'):
			from .Reflection import Reflection
			self._reflection = Reflection(self._core, self._cmd_group)
		return self._reflection

	@property
	def swr(self):
		"""swr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_swr'):
			from .Swr import Swr
			self._swr = Swr(self._core, self._cmd_group)
		return self._swr

	def clone(self) -> 'Limit':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Limit(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
