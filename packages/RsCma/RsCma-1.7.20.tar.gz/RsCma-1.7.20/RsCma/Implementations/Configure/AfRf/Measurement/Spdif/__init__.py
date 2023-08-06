from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spdif:
	"""Spdif commands group definition. 27 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spdif", core, parent)

	@property
	def level(self):
		"""level commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Level import Level
			self._level = Level(self._core, self._cmd_group)
		return self._level

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import Frequency
			self._frequency = Frequency(self._core, self._cmd_group)
		return self._frequency

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import Delay
			self._delay = Delay(self._core, self._cmd_group)
		return self._delay

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import Enable
			self._enable = Enable(self._core, self._cmd_group)
		return self._enable

	@property
	def gcoupling(self):
		"""gcoupling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gcoupling'):
			from .Gcoupling import Gcoupling
			self._gcoupling = Gcoupling(self._core, self._cmd_group)
		return self._gcoupling

	@property
	def tmode(self):
		"""tmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmode'):
			from .Tmode import Tmode
			self._tmode = Tmode(self._core, self._cmd_group)
		return self._tmode

	@property
	def filterPy(self):
		"""filterPy commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._cmd_group)
		return self._filterPy

	def clone(self) -> 'Spdif':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Spdif(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
