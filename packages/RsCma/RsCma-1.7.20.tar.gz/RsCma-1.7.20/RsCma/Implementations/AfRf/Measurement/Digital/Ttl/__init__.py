from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ttl:
	"""Ttl commands group definition. 11 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ttl", core, parent)

	@property
	def bitErrorRate(self):
		"""bitErrorRate commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_bitErrorRate'):
			from .BitErrorRate import BitErrorRate
			self._bitErrorRate = BitErrorRate(self._core, self._cmd_group)
		return self._bitErrorRate

	def clone(self) -> 'Ttl':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ttl(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
