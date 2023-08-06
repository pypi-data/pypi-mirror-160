from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SignalQuality:
	"""SignalQuality commands group definition. 72 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("signalQuality", core, parent)

	@property
	def demodLeft(self):
		"""demodLeft commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodLeft'):
			from .DemodLeft import DemodLeft
			self._demodLeft = DemodLeft(self._core, self._cmd_group)
		return self._demodLeft

	@property
	def demodRight(self):
		"""demodRight commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodRight'):
			from .DemodRight import DemodRight
			self._demodRight = DemodRight(self._core, self._cmd_group)
		return self._demodRight

	@property
	def audioInput(self):
		"""audioInput commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._cmd_group)
		return self._audioInput

	@property
	def spdifLeft(self):
		"""spdifLeft commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdifLeft'):
			from .SpdifLeft import SpdifLeft
			self._spdifLeft = SpdifLeft(self._core, self._cmd_group)
		return self._spdifLeft

	@property
	def spdifRight(self):
		"""spdifRight commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdifRight'):
			from .SpdifRight import SpdifRight
			self._spdifRight = SpdifRight(self._core, self._cmd_group)
		return self._spdifRight

	@property
	def voip(self):
		"""voip commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_voip'):
			from .Voip import Voip
			self._voip = Voip(self._core, self._cmd_group)
		return self._voip

	def clone(self) -> 'SignalQuality':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SignalQuality(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
