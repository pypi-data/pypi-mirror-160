from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Symbols:
	"""Symbols commands group definition. 4 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("symbols", core, parent)

	@property
	def hexadecimal(self):
		"""hexadecimal commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_hexadecimal'):
			from .Hexadecimal import Hexadecimal
			self._hexadecimal = Hexadecimal(self._core, self._cmd_group)
		return self._hexadecimal

	@property
	def binary(self):
		"""binary commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_binary'):
			from .Binary import Binary
			self._binary = Binary(self._core, self._cmd_group)
		return self._binary

	def clone(self) -> 'Symbols':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Symbols(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
