from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tetra:
	"""Tetra commands group definition. 13 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tetra", core, parent)

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

	@property
	def sinfo(self):
		"""sinfo commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sinfo'):
			from .Sinfo import Sinfo
			self._sinfo = Sinfo(self._core, self._cmd_group)
		return self._sinfo

	@property
	def freqError(self):
		"""freqError commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_freqError'):
			from .FreqError import FreqError
			self._freqError = FreqError(self._core, self._cmd_group)
		return self._freqError

	def clone(self) -> 'Tetra':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tetra(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
