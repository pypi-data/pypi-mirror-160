from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vor:
	"""Vor commands group definition. 21 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vor", core, parent)

	@property
	def afSettings(self):
		"""afSettings commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_afSettings'):
			from .AfSettings import AfSettings
			self._afSettings = AfSettings(self._core, self._cmd_group)
		return self._afSettings

	@property
	def rfSettings(self):
		"""rfSettings commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_rfSettings'):
			from .RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._cmd_group)
		return self._rfSettings

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._cmd_group)
		return self._state

	@property
	def idSignal(self):
		"""idSignal commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_idSignal'):
			from .IdSignal import IdSignal
			self._idSignal = IdSignal(self._core, self._cmd_group)
		return self._idSignal

	def clone(self) -> 'Vor':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Vor(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
