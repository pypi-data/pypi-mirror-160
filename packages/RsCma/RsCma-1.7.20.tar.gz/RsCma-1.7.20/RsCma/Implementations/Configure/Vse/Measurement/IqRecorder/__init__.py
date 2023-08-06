from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqRecorder:
	"""IqRecorder commands group definition. 8 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqRecorder", core, parent)

	@property
	def lte(self):
		"""lte commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_lte'):
			from .Lte import Lte
			self._lte = Lte(self._core, self._cmd_group)
		return self._lte

	@property
	def capture(self):
		"""capture commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_capture'):
			from .Capture import Capture
			self._capture = Capture(self._core, self._cmd_group)
		return self._capture

	@property
	def ratio(self):
		"""ratio commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ratio'):
			from .Ratio import Ratio
			self._ratio = Ratio(self._core, self._cmd_group)
		return self._ratio

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._cmd_group)
		return self._symbolRate

	@property
	def munit(self):
		"""munit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_munit'):
			from .Munit import Munit
			self._munit = Munit(self._core, self._cmd_group)
		return self._munit

	@property
	def filterPy(self):
		"""filterPy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._cmd_group)
		return self._filterPy

	def clone(self) -> 'IqRecorder':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqRecorder(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
