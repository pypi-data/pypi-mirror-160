from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Oscilloscope:
	"""Oscilloscope commands group definition. 35 total commands, 5 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("oscilloscope", core, parent)

	@property
	def timeout(self):
		"""timeout commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_timeout'):
			from .Timeout import Timeout
			self._timeout = Timeout(self._core, self._cmd_group)
		return self._timeout

	@property
	def demodulation(self):
		"""demodulation commands group. 4 Sub-classes, 7 commands."""
		if not hasattr(self, '_demodulation'):
			from .Demodulation import Demodulation
			self._demodulation = Demodulation(self._core, self._cmd_group)
		return self._demodulation

	@property
	def audioInput(self):
		"""audioInput commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_audioInput'):
			from .AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._cmd_group)
		return self._audioInput

	@property
	def spdif(self):
		"""spdif commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_spdif'):
			from .Spdif import Spdif
			self._spdif = Spdif(self._core, self._cmd_group)
		return self._spdif

	@property
	def voip(self):
		"""voip commands group. 0 Sub-classes, 7 commands."""
		if not hasattr(self, '_voip'):
			from .Voip import Voip
			self._voip = Voip(self._core, self._cmd_group)
		return self._voip

	def clone(self) -> 'Oscilloscope':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Oscilloscope(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
