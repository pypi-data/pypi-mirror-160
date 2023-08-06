from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Measurement:
	"""Measurement commands group definition. 4 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("measurement", core, parent)

	@property
	def application(self):
		"""application commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_application'):
			from .Application import Application
			self._application = Application(self._core, self._cmd_group)
		return self._application

	@property
	def routines(self):
		"""routines commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_routines'):
			from .Routines import Routines
			self._routines = Routines(self._core, self._cmd_group)
		return self._routines

	@property
	def digital(self):
		"""digital commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_digital'):
			from .Digital import Digital
			self._digital = Digital(self._core, self._cmd_group)
		return self._digital

	@property
	def audio(self):
		"""audio commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_audio'):
			from .Audio import Audio
			self._audio = Audio(self._core, self._cmd_group)
		return self._audio

	def clone(self) -> 'Measurement':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Measurement(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
