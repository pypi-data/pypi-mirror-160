from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voip:
	"""Voip commands group definition. 6 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("voip", core, parent)

	@property
	def thDistortion(self):
		"""thDistortion commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_thDistortion'):
			from .ThDistortion import ThDistortion
			self._thDistortion = ThDistortion(self._core, self._cmd_group)
		return self._thDistortion

	@property
	def thdNoise(self):
		"""thdNoise commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_thdNoise'):
			from .ThdNoise import ThdNoise
			self._thdNoise = ThdNoise(self._core, self._cmd_group)
		return self._thdNoise

	@property
	def snRatio(self):
		"""snRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snRatio'):
			from .SnRatio import SnRatio
			self._snRatio = SnRatio(self._core, self._cmd_group)
		return self._snRatio

	@property
	def snnRatio(self):
		"""snnRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_snnRatio'):
			from .SnnRatio import SnnRatio
			self._snnRatio = SnnRatio(self._core, self._cmd_group)
		return self._snnRatio

	@property
	def sndRatio(self):
		"""sndRatio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sndRatio'):
			from .SndRatio import SndRatio
			self._sndRatio = SndRatio(self._core, self._cmd_group)
		return self._sndRatio

	@property
	def sinad(self):
		"""sinad commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sinad'):
			from .Sinad import Sinad
			self._sinad = Sinad(self._core, self._cmd_group)
		return self._sinad

	def clone(self) -> 'Voip':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Voip(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
