from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tones:
	"""Tones commands group definition. 9 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tones", core, parent)

	@property
	def scal(self):
		"""scal commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_scal'):
			from .Scal import Scal
			self._scal = Scal(self._core, self._cmd_group)
		return self._scal

	@property
	def dcs(self):
		"""dcs commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcs'):
			from .Dcs import Dcs
			self._dcs = Dcs(self._core, self._cmd_group)
		return self._dcs

	@property
	def digPause(self):
		"""digPause commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_digPause'):
			from .DigPause import DigPause
			self._digPause = DigPause(self._core, self._cmd_group)
		return self._digPause

	@property
	def digtime(self):
		"""digtime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_digtime'):
			from .Digtime import Digtime
			self._digtime = Digtime(self._core, self._cmd_group)
		return self._digtime

	@property
	def fdeviation(self):
		"""fdeviation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._cmd_group)
		return self._fdeviation

	def clone(self) -> 'Tones':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tones(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
