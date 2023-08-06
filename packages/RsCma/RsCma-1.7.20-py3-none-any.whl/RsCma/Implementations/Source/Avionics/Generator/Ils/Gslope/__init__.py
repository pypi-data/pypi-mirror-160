from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gslope:
	"""Gslope commands group definition. 15 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gslope", core, parent)

	@property
	def afSettings(self):
		"""afSettings commands group. 3 Sub-classes, 6 commands."""
		if not hasattr(self, '_afSettings'):
			from .AfSettings import AfSettings
			self._afSettings = AfSettings(self._core, self._cmd_group)
		return self._afSettings

	@property
	def rfSettings(self):
		"""rfSettings commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_rfSettings'):
			from .RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._cmd_group)
		return self._rfSettings

	def clone(self) -> 'Gslope':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gslope(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
