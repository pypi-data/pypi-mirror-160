from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ZeroSpan:
	"""ZeroSpan commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("zeroSpan", core, parent)

	@property
	def marker(self):
		"""marker commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import Marker
			self._marker = Marker(self._core, self._cmd_group)
		return self._marker

	@property
	def xvalues(self):
		"""xvalues commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_xvalues'):
			from .Xvalues import Xvalues
			self._xvalues = Xvalues(self._core, self._cmd_group)
		return self._xvalues

	def clone(self) -> 'ZeroSpan':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ZeroSpan(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
