from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voip:
	"""Voip commands group definition. 42 total commands, 7 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("voip", core, parent)

	@property
	def level(self):
		"""level commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Level import Level
			self._level = Level(self._core, self._cmd_group)
		return self._level

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import Frequency
			self._frequency = Frequency(self._core, self._cmd_group)
		return self._frequency

	@property
	def uri(self):
		"""uri commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_uri'):
			from .Uri import Uri
			self._uri = Uri(self._core, self._cmd_group)
		return self._uri

	@property
	def sip(self):
		"""sip commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_sip'):
			from .Sip import Sip
			self._sip = Sip(self._core, self._cmd_group)
		return self._sip

	@property
	def squelch(self):
		"""squelch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_squelch'):
			from .Squelch import Squelch
			self._squelch = Squelch(self._core, self._cmd_group)
		return self._squelch

	@property
	def rssi(self):
		"""rssi commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rssi'):
			from .Rssi import Rssi
			self._rssi = Rssi(self._core, self._cmd_group)
		return self._rssi

	@property
	def filterPy(self):
		"""filterPy commands group. 3 Sub-classes, 5 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._cmd_group)
		return self._filterPy

	def get_delay(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:DELay \n
		Snippet: value: bool = driver.configure.afRf.measurement.voip.get_delay() \n
		No command help available \n
			:return: audio_delay: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:DELay?')
		return Conversions.str_to_bool(response)

	def set_delay(self, audio_delay: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:DELay \n
		Snippet: driver.configure.afRf.measurement.voip.set_delay(audio_delay = False) \n
		No command help available \n
			:param audio_delay: No help available
		"""
		param = Conversions.bool_to_str(audio_delay)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:DELay {param}')

	# noinspection PyTypeChecker
	def get_gcoupling(self) -> enums.GeneratorCouplingVoIp:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:GCOupling \n
		Snippet: value: enums.GeneratorCouplingVoIp = driver.configure.afRf.measurement.voip.get_gcoupling() \n
		Couples the audio output of the VoIP input path to an internal signal generator. \n
			:return: coupling: OFF | GEN3 | GEN4 OFF No coupling GEN3 Coupled to audio generator 3 GEN4 Coupled to audio generator 4
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:GCOupling?')
		return Conversions.str_to_scalar_enum(response, enums.GeneratorCouplingVoIp)

	def set_gcoupling(self, coupling: enums.GeneratorCouplingVoIp) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:GCOupling \n
		Snippet: driver.configure.afRf.measurement.voip.set_gcoupling(coupling = enums.GeneratorCouplingVoIp.GEN3) \n
		Couples the audio output of the VoIP input path to an internal signal generator. \n
			:param coupling: OFF | GEN3 | GEN4 OFF No coupling GEN3 Coupled to audio generator 3 GEN4 Coupled to audio generator 4
		"""
		param = Conversions.enum_scalar_to_str(coupling, enums.GeneratorCouplingVoIp)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:GCOupling {param}')

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.voip.get_enable() \n
		Enables or disables the audio signal output of the VoIP input path. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:ENABle \n
		Snippet: driver.configure.afRf.measurement.voip.set_enable(enable = False) \n
		Enables or disables the audio signal output of the VoIP input path. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:ENABle {param}')

	# noinspection PyTypeChecker
	def get_pcodec(self) -> enums.VoIpCodec:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:PCODec \n
		Snippet: value: enums.VoIpCodec = driver.configure.afRf.measurement.voip.get_pcodec() \n
		Queries the type of the pulse code modulation (PCM) codec. \n
			:return: pcodec: ALAW | ULAW A-law codec or µ-law codec
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:PCODec?')
		return Conversions.str_to_scalar_enum(response, enums.VoIpCodec)

	def get_fid(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FID \n
		Snippet: value: float = driver.configure.afRf.measurement.voip.get_fid() \n
		Specifies the frequency ID (FID) configured at the DUT.
			INTRO_CMD_HELP: Allowed values are, with n = 0 to 39995: \n
			- 0.100 + n * 0.025
			- 0.105 + n * 0.025
			- 0.110 + n * 0.025
			- 0.115 + n * 0.025
		Resulting in: 0.100, 0.105, 0.110, 0.115, 0.125, 0.130, 0.135, 0.140, ..., 999.975, 999.980, 999.985, 999.990 \n
			:return: frequency_id: Frequency ID Not allowed values are rounded to the closest allowed value. Range: 0.1 to 999.99
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:FID?')
		return Conversions.str_to_float(response)

	def set_fid(self, frequency_id: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FID \n
		Snippet: driver.configure.afRf.measurement.voip.set_fid(frequency_id = 1.0) \n
		Specifies the frequency ID (FID) configured at the DUT.
			INTRO_CMD_HELP: Allowed values are, with n = 0 to 39995: \n
			- 0.100 + n * 0.025
			- 0.105 + n * 0.025
			- 0.110 + n * 0.025
			- 0.115 + n * 0.025
		Resulting in: 0.100, 0.105, 0.110, 0.115, 0.125, 0.130, 0.135, 0.140, ..., 999.975, 999.980, 999.985, 999.990 \n
			:param frequency_id: Frequency ID Not allowed values are rounded to the closest allowed value. Range: 0.1 to 999.99
		"""
		param = Conversions.decimal_value_to_str(frequency_id)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FID {param}')

	def clone(self) -> 'Voip':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Voip(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
