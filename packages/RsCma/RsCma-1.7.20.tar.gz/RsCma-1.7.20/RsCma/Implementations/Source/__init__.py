from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 334 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	@property
	def afRf(self):
		"""afRf commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_afRf'):
			from .AfRf import AfRf
			self._afRf = AfRf(self._core, self._cmd_group)
		return self._afRf

	@property
	def xrt(self):
		"""xrt commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_xrt'):
			from .Xrt import Xrt
			self._xrt = Xrt(self._core, self._cmd_group)
		return self._xrt

	@property
	def avionics(self):
		"""avionics commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_avionics'):
			from .Avionics import Avionics
			self._avionics = Avionics(self._core, self._cmd_group)
		return self._avionics

	@property
	def base(self):
		"""base commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_base'):
			from .Base import Base
			self._base = Base(self._core, self._cmd_group)
		return self._base

	def clone(self) -> 'Source':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Source(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
