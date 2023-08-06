from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Calibration:
	"""Calibration commands group definition. 7 total commands, 2 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("calibration", core, parent)

	@property
	def base(self):
		"""base commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_base'):
			from .Base import Base
			self._base = Base(self._core, self._cmd_group)
		return self._base

	@property
	def gprfMeasurement(self):
		"""gprfMeasurement commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_gprfMeasurement'):
			from .GprfMeasurement import GprfMeasurement
			self._gprfMeasurement = GprfMeasurement(self._core, self._cmd_group)
		return self._gprfMeasurement

	def clone(self) -> 'Calibration':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Calibration(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
