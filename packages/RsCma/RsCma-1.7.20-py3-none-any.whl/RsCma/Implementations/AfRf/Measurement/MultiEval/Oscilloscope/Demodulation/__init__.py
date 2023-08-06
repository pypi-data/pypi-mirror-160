from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 8 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("demodulation", core, parent)

	@property
	def pdeviation(self):
		"""pdeviation commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdeviation'):
			from .Pdeviation import Pdeviation
			self._pdeviation = Pdeviation(self._core, self._cmd_group)
		return self._pdeviation

	@property
	def modDepth(self):
		"""modDepth commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_modDepth'):
			from .ModDepth import ModDepth
			self._modDepth = ModDepth(self._core, self._cmd_group)
		return self._modDepth

	@property
	def lsbLevel(self):
		"""lsbLevel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_lsbLevel'):
			from .LsbLevel import LsbLevel
			self._lsbLevel = LsbLevel(self._core, self._cmd_group)
		return self._lsbLevel

	@property
	def usbLevel(self):
		"""usbLevel commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_usbLevel'):
			from .UsbLevel import UsbLevel
			self._usbLevel = UsbLevel(self._core, self._cmd_group)
		return self._usbLevel

	def clone(self) -> 'Demodulation':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Demodulation(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
