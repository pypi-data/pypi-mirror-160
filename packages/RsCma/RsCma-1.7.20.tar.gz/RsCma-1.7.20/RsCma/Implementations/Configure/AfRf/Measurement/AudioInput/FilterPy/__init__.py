from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 11 total commands, 8 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	@property
	def dwidth(self):
		"""dwidth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dwidth'):
			from .Dwidth import Dwidth
			self._dwidth = Dwidth(self._core, self._cmd_group)
		return self._dwidth

	@property
	def bpass(self):
		"""bpass commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_bpass'):
			from .Bpass import Bpass
			self._bpass = Bpass(self._core, self._cmd_group)
		return self._bpass

	@property
	def weighting(self):
		"""weighting commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_weighting'):
			from .Weighting import Weighting
			self._weighting = Weighting(self._core, self._cmd_group)
		return self._weighting

	@property
	def dfrequency(self):
		"""dfrequency commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dfrequency'):
			from .Dfrequency import Dfrequency
			self._dfrequency = Dfrequency(self._core, self._cmd_group)
		return self._dfrequency

	@property
	def robustAuto(self):
		"""robustAuto commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_robustAuto'):
			from .RobustAuto import RobustAuto
			self._robustAuto = RobustAuto(self._core, self._cmd_group)
		return self._robustAuto

	@property
	def notch(self):
		"""notch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_notch'):
			from .Notch import Notch
			self._notch = Notch(self._core, self._cmd_group)
		return self._notch

	@property
	def lpass(self):
		"""lpass commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lpass'):
			from .Lpass import Lpass
			self._lpass = Lpass(self._core, self._cmd_group)
		return self._lpass

	@property
	def hpass(self):
		"""hpass commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hpass'):
			from .Hpass import Hpass
			self._hpass = Hpass(self._core, self._cmd_group)
		return self._hpass

	def clone(self) -> 'FilterPy':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPy(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
