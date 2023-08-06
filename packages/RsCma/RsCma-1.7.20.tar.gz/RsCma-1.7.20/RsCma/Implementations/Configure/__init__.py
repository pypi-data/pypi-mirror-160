from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Configure:
	"""Configure commands group definition. 609 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("configure", core, parent)

	@property
	def afRf(self):
		"""afRf commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_afRf'):
			from .AfRf import AfRf
			self._afRf = AfRf(self._core, self._cmd_group)
		return self._afRf

	@property
	def base(self):
		"""base commands group. 11 Sub-classes, 2 commands."""
		if not hasattr(self, '_base'):
			from .Base import Base
			self._base = Base(self._core, self._cmd_group)
		return self._base

	@property
	def sequencer(self):
		"""sequencer commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_sequencer'):
			from .Sequencer import Sequencer
			self._sequencer = Sequencer(self._core, self._cmd_group)
		return self._sequencer

	@property
	def gprfMeasurement(self):
		"""gprfMeasurement commands group. 8 Sub-classes, 1 commands."""
		if not hasattr(self, '_gprfMeasurement'):
			from .GprfMeasurement import GprfMeasurement
			self._gprfMeasurement = GprfMeasurement(self._core, self._cmd_group)
		return self._gprfMeasurement

	@property
	def display(self):
		"""display commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_display'):
			from .Display import Display
			self._display = Display(self._core, self._cmd_group)
		return self._display

	@property
	def vse(self):
		"""vse commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_vse'):
			from .Vse import Vse
			self._vse = Vse(self._core, self._cmd_group)
		return self._vse

	def clone(self) -> 'Configure':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Configure(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
