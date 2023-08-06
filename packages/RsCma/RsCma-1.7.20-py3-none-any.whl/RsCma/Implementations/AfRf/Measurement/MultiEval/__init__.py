from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiEval:
	"""MultiEval commands group definition. 506 total commands, 13 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("multiEval", core, parent)

	@property
	def audioInput(self):
		"""audioInput commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._cmd_group)
		return self._audioInput

	@property
	def spdifLeft(self):
		"""spdifLeft commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdifLeft'):
			from .SpdifLeft import SpdifLeft
			self._spdifLeft = SpdifLeft(self._core, self._cmd_group)
		return self._spdifLeft

	@property
	def spdifRight(self):
		"""spdifRight commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdifRight'):
			from .SpdifRight import SpdifRight
			self._spdifRight = SpdifRight(self._core, self._cmd_group)
		return self._spdifRight

	@property
	def voip(self):
		"""voip commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_voip'):
			from .Voip import Voip
			self._voip = Voip(self._core, self._cmd_group)
		return self._voip

	@property
	def demodLeft(self):
		"""demodLeft commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodLeft'):
			from .DemodLeft import DemodLeft
			self._demodLeft = DemodLeft(self._core, self._cmd_group)
		return self._demodLeft

	@property
	def demodRight(self):
		"""demodRight commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodRight'):
			from .DemodRight import DemodRight
			self._demodRight = DemodRight(self._core, self._cmd_group)
		return self._demodRight

	@property
	def demodulation(self):
		"""demodulation commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodulation'):
			from .Demodulation import Demodulation
			self._demodulation = Demodulation(self._core, self._cmd_group)
		return self._demodulation

	@property
	def rfCarrier(self):
		"""rfCarrier commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_rfCarrier'):
			from .RfCarrier import RfCarrier
			self._rfCarrier = RfCarrier(self._core, self._cmd_group)
		return self._rfCarrier

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._cmd_group)
		return self._state

	@property
	def oscilloscope(self):
		"""oscilloscope commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_oscilloscope'):
			from .Oscilloscope import Oscilloscope
			self._oscilloscope = Oscilloscope(self._core, self._cmd_group)
		return self._oscilloscope

	@property
	def signalQuality(self):
		"""signalQuality commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_signalQuality'):
			from .SignalQuality import SignalQuality
			self._signalQuality = SignalQuality(self._core, self._cmd_group)
		return self._signalQuality

	@property
	def tones(self):
		"""tones commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_tones'):
			from .Tones import Tones
			self._tones = Tones(self._core, self._cmd_group)
		return self._tones

	@property
	def fft(self):
		"""fft commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_fft'):
			from .Fft import Fft
			self._fft = Fft(self._core, self._cmd_group)
		return self._fft

	def initiate(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INITiate:AFRF:MEASurement<Instance>:MEValuation \n
		Snippet: driver.afRf.measurement.multiEval.initiate() \n
		Starts or continues the analyzer. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INITiate:AFRF:MEASurement<Instance>:MEValuation', opc_timeout_ms)

	def stop(self) -> None:
		"""SCPI: STOP:AFRF:MEASurement<Instance>:MEValuation \n
		Snippet: driver.afRf.measurement.multiEval.stop() \n
		Pauses the analyzer. \n
		"""
		self._core.io.write(f'STOP:AFRF:MEASurement<Instance>:MEValuation')

	def stop_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: STOP:AFRF:MEASurement<Instance>:MEValuation \n
		Snippet: driver.afRf.measurement.multiEval.stop_with_opc() \n
		Pauses the analyzer. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'STOP:AFRF:MEASurement<Instance>:MEValuation', opc_timeout_ms)

	def abort(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: ABORt:AFRF:MEASurement<Instance>:MEValuation \n
		Snippet: driver.afRf.measurement.multiEval.abort() \n
		Stops the analyzer. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'ABORt:AFRF:MEASurement<Instance>:MEValuation', opc_timeout_ms)

	def clone(self) -> 'MultiEval':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiEval(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
