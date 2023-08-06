from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 76 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("demodulation", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import Frequency
			self._frequency = Frequency(self._core, self._cmd_group)
		return self._frequency

	@property
	def modDepth(self):
		"""modDepth commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_modDepth'):
			from .ModDepth import ModDepth
			self._modDepth = ModDepth(self._core, self._cmd_group)
		return self._modDepth

	@property
	def fdeviation(self):
		"""fdeviation commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._cmd_group)
		return self._fdeviation

	@property
	def fmStereo(self):
		"""fmStereo commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_fmStereo'):
			from .FmStereo import FmStereo
			self._fmStereo = FmStereo(self._core, self._cmd_group)
		return self._fmStereo

	@property
	def pdeviation(self):
		"""pdeviation commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdeviation'):
			from .Pdeviation import Pdeviation
			self._pdeviation = Pdeviation(self._core, self._cmd_group)
		return self._pdeviation

	def clone(self) -> 'Demodulation':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Demodulation(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
