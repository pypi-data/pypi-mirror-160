from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Generator:
	"""Generator commands group definition. 74 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("generator", core, parent)

	@property
	def rfSettings(self):
		"""rfSettings commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rfSettings'):
			from .RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._cmd_group)
		return self._rfSettings

	@property
	def vor(self):
		"""vor commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_vor'):
			from .Vor import Vor
			self._vor = Vor(self._core, self._cmd_group)
		return self._vor

	@property
	def ils(self):
		"""ils commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_ils'):
			from .Ils import Ils
			self._ils = Ils(self._core, self._cmd_group)
		return self._ils

	@property
	def markerBeacon(self):
		"""markerBeacon commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_markerBeacon'):
			from .MarkerBeacon import MarkerBeacon
			self._markerBeacon = MarkerBeacon(self._core, self._cmd_group)
		return self._markerBeacon

	def clone(self) -> 'Generator':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Generator(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
