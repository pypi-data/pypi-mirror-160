from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 3 total commands, 3 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	@property
	def typePy(self):
		"""typePy commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_typePy'):
			from .TypePy import TypePy
			self._typePy = TypePy(self._core, self._cmd_group)
		return self._typePy

	@property
	def bandpass(self):
		"""bandpass commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_bandpass'):
			from .Bandpass import Bandpass
			self._bandpass = Bandpass(self._core, self._cmd_group)
		return self._bandpass

	@property
	def gauss(self):
		"""gauss commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_gauss'):
			from .Gauss import Gauss
			self._gauss = Gauss(self._core, self._cmd_group)
		return self._gauss

	def clone(self) -> 'FilterPy':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPy(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
