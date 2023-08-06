from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmr:
	"""Dmr commands group definition. 12 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmr", core, parent)

	@property
	def poOff(self):
		"""poOff commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_poOff'):
			from .PoOff import PoOff
			self._poOff = PoOff(self._core, self._cmd_group)
		return self._poOff

	@property
	def sinfo(self):
		"""sinfo commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sinfo'):
			from .Sinfo import Sinfo
			self._sinfo = Sinfo(self._core, self._cmd_group)
		return self._sinfo

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .Power import Power
			self._power = Power(self._core, self._cmd_group)
		return self._power

	@property
	def bitErrorRate(self):
		"""bitErrorRate commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bitErrorRate'):
			from .BitErrorRate import BitErrorRate
			self._bitErrorRate = BitErrorRate(self._core, self._cmd_group)
		return self._bitErrorRate

	def clone(self) -> 'Dmr':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dmr(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
