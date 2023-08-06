from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class GprfMeasurement:
	"""GprfMeasurement commands group definition. 119 total commands, 8 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gprfMeasurement", core, parent)

	@property
	def spectrum(self):
		"""spectrum commands group. 6 Sub-classes, 5 commands."""
		if not hasattr(self, '_spectrum'):
			from .Spectrum import Spectrum
			self._spectrum = Spectrum(self._core, self._cmd_group)
		return self._spectrum

	@property
	def iqRecorder(self):
		"""iqRecorder commands group. 2 Sub-classes, 8 commands."""
		if not hasattr(self, '_iqRecorder'):
			from .IqRecorder import IqRecorder
			self._iqRecorder = IqRecorder(self._core, self._cmd_group)
		return self._iqRecorder

	@property
	def rfSettings(self):
		"""rfSettings commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_rfSettings'):
			from .RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._cmd_group)
		return self._rfSettings

	@property
	def extPwrSensor(self):
		"""extPwrSensor commands group. 2 Sub-classes, 6 commands."""
		if not hasattr(self, '_extPwrSensor'):
			from .ExtPwrSensor import ExtPwrSensor
			self._extPwrSensor = ExtPwrSensor(self._core, self._cmd_group)
		return self._extPwrSensor

	@property
	def nrt(self):
		"""nrt commands group. 3 Sub-classes, 10 commands."""
		if not hasattr(self, '_nrt'):
			from .Nrt import Nrt
			self._nrt = Nrt(self._core, self._cmd_group)
		return self._nrt

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_power'):
			from .Power import Power
			self._power = Power(self._core, self._cmd_group)
		return self._power

	@property
	def fftSpecAn(self):
		"""fftSpecAn commands group. 2 Sub-classes, 9 commands."""
		if not hasattr(self, '_fftSpecAn'):
			from .FftSpecAn import FftSpecAn
			self._fftSpecAn = FftSpecAn(self._core, self._cmd_group)
		return self._fftSpecAn

	@property
	def acp(self):
		"""acp commands group. 2 Sub-classes, 8 commands."""
		if not hasattr(self, '_acp'):
			from .Acp import Acp
			self._acp = Acp(self._core, self._cmd_group)
		return self._acp

	def get_crepetition(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:CREPetition \n
		Snippet: value: bool = driver.configure.gprfMeasurement.get_crepetition() \n
		Enables or disables the automatic configuration of the repetition mode. With enabled automatic configuration, the
		repetition mode of all measurements is set to 'Continuous' each time the instrument switches from remote operation to
		manual operation. \n
			:return: continuous_repetition: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:CREPetition?')
		return Conversions.str_to_bool(response)

	def set_crepetition(self, continuous_repetition: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:CREPetition \n
		Snippet: driver.configure.gprfMeasurement.set_crepetition(continuous_repetition = False) \n
		Enables or disables the automatic configuration of the repetition mode. With enabled automatic configuration, the
		repetition mode of all measurements is set to 'Continuous' each time the instrument switches from remote operation to
		manual operation. \n
			:param continuous_repetition: OFF | ON
		"""
		param = Conversions.bool_to_str(continuous_repetition)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:CREPetition {param}')

	def clone(self) -> 'GprfMeasurement':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = GprfMeasurement(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
