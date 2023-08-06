from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Scal:
	"""Scal commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("scal", core, parent)

	@property
	def fdeviation(self):
		"""fdeviation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._cmd_group)
		return self._fdeviation

	@property
	def ttime(self):
		"""ttime commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttime'):
			from .Ttime import Ttime
			self._ttime = Ttime(self._core, self._cmd_group)
		return self._ttime

	@property
	def tpause(self):
		"""tpause commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tpause'):
			from .Tpause import Tpause
			self._tpause = Tpause(self._core, self._cmd_group)
		return self._tpause

	def clone(self) -> 'Scal':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Scal(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
