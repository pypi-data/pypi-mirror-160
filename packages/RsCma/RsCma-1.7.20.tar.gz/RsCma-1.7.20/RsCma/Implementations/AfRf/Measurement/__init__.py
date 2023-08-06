from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Measurement:
	"""Measurement commands group definition. 639 total commands, 7 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("measurement", core, parent)

	@property
	def digital(self):
		"""digital commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_digital'):
			from .Digital import Digital
			self._digital = Digital(self._core, self._cmd_group)
		return self._digital

	@property
	def multiEval(self):
		"""multiEval commands group. 13 Sub-classes, 3 commands."""
		if not hasattr(self, '_multiEval'):
			from .MultiEval import MultiEval
			self._multiEval = MultiEval(self._core, self._cmd_group)
		return self._multiEval

	@property
	def searchRoutines(self):
		"""searchRoutines commands group. 7 Sub-classes, 3 commands."""
		if not hasattr(self, '_searchRoutines'):
			from .SearchRoutines import SearchRoutines
			self._searchRoutines = SearchRoutines(self._core, self._cmd_group)
		return self._searchRoutines

	@property
	def audioInput(self):
		"""audioInput commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._cmd_group)
		return self._audioInput

	@property
	def spdif(self):
		"""spdif commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdif'):
			from .Spdif import Spdif
			self._spdif = Spdif(self._core, self._cmd_group)
		return self._spdif

	@property
	def voip(self):
		"""voip commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_voip'):
			from .Voip import Voip
			self._voip = Voip(self._core, self._cmd_group)
		return self._voip

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import Frequency
			self._frequency = Frequency(self._core, self._cmd_group)
		return self._frequency

	def clone(self) -> 'Measurement':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Measurement(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
