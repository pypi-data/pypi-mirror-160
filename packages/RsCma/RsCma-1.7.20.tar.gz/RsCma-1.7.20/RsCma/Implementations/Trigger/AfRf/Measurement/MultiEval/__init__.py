from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiEval:
	"""MultiEval commands group definition. 35 total commands, 1 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("multiEval", core, parent)

	@property
	def oscilloscope(self):
		"""oscilloscope commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_oscilloscope'):
			from .Oscilloscope import Oscilloscope
			self._oscilloscope = Oscilloscope(self._core, self._cmd_group)
		return self._oscilloscope

	def clone(self) -> 'MultiEval':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiEval(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
