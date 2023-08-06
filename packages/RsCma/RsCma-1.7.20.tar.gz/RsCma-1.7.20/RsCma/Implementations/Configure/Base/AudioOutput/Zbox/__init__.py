from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Zbox:
	"""Zbox commands group definition. 1 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("zbox", core, parent)

	@property
	def impedance(self):
		"""impedance commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_impedance'):
			from .Impedance import Impedance
			self._impedance = Impedance(self._core, self._cmd_group)
		return self._impedance

	def clone(self) -> 'Zbox':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Zbox(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
