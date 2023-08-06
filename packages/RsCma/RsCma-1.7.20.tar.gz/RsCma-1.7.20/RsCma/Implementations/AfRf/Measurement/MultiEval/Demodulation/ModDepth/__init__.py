from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModDepth:
	"""ModDepth commands group definition. 16 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("modDepth", core, parent)

	@property
	def delta(self):
		"""delta commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_delta'):
			from .Delta import Delta
			self._delta = Delta(self._core, self._cmd_group)
		return self._delta

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_current'):
			from .Current import Current
			self._current = Current(self._core, self._cmd_group)
		return self._current

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_average'):
			from .Average import Average
			self._average = Average(self._core, self._cmd_group)
		return self._average

	@property
	def maximum(self):
		"""maximum commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_maximum'):
			from .Maximum import Maximum
			self._maximum = Maximum(self._core, self._cmd_group)
		return self._maximum

	@property
	def deviation(self):
		"""deviation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_deviation'):
			from .Deviation import Deviation
			self._deviation = Deviation(self._core, self._cmd_group)
		return self._deviation

	def clone(self) -> 'ModDepth':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ModDepth(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
