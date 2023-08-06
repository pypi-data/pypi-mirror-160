from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GprfMeasurement:
	"""GprfMeasurement commands group definition. 5 total commands, 4 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gprfMeasurement", core, parent)

	@property
	def extPwrSensor(self):
		"""extPwrSensor commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_extPwrSensor'):
			from .ExtPwrSensor import ExtPwrSensor
			self._extPwrSensor = ExtPwrSensor(self._core, self._cmd_group)
		return self._extPwrSensor

	@property
	def spectrum(self):
		"""spectrum commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_spectrum'):
			from .Spectrum import Spectrum
			self._spectrum = Spectrum(self._core, self._cmd_group)
		return self._spectrum

	@property
	def fftSpecAn(self):
		"""fftSpecAn commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fftSpecAn'):
			from .FftSpecAn import FftSpecAn
			self._fftSpecAn = FftSpecAn(self._core, self._cmd_group)
		return self._fftSpecAn

	@property
	def acp(self):
		"""acp commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_acp'):
			from .Acp import Acp
			self._acp = Acp(self._core, self._cmd_group)
		return self._acp

	def clone(self) -> 'GprfMeasurement':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GprfMeasurement(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
