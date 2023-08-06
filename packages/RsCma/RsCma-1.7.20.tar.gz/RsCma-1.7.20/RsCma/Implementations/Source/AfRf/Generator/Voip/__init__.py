from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voip:
	"""Voip commands group definition. 20 total commands, 3 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("voip", core, parent)

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
	def ptt(self):
		"""ptt commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ptt'):
			from .Ptt import Ptt
			self._ptt = Ptt(self._core, self._cmd_group)
		return self._ptt

	def get_delay(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:DELay \n
		Snippet: value: bool = driver.source.afRf.generator.voip.get_delay() \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:DELay?')
		return Conversions.str_to_bool(response)

	def set_delay(self, delay: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:DELay \n
		Snippet: driver.source.afRf.generator.voip.set_delay(delay = False) \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.bool_to_str(delay)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:VOIP:DELay {param}')

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.voip.get_enable() \n
		Enables or disables VoIP. \n
			:return: vo_ip_enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, vo_ip_enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:ENABle \n
		Snippet: driver.source.afRf.generator.voip.set_enable(vo_ip_enable = False) \n
		Enables or disables VoIP. \n
			:param vo_ip_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(vo_ip_enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:VOIP:ENABle {param}')

	# noinspection PyTypeChecker
	def get_pcodec(self) -> enums.VoIpCodec:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:PCODec \n
		Snippet: value: enums.VoIpCodec = driver.source.afRf.generator.voip.get_pcodec() \n
		Queries the type of the pulse code modulation (PCM) codec. \n
			:return: vo_ip_codec: ALAW
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:PCODec?')
		return Conversions.str_to_scalar_enum(response, enums.VoIpCodec)

	def get_level(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:LEVel \n
		Snippet: value: float = driver.source.afRf.generator.voip.get_level() \n
		Specifies the audio output level for the VoIP path. For noise signals provided by an internal generator, the maximum
		allowed level is reduced by the factor 1/sqrt(2) . \n
			:return: level: Range: 0.01 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:LEVel \n
		Snippet: driver.source.afRf.generator.voip.set_level(level = 1.0) \n
		Specifies the audio output level for the VoIP path. For noise signals provided by an internal generator, the maximum
		allowed level is reduced by the factor 1/sqrt(2) . \n
			:param level: Range: 0.01 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:VOIP:LEVel {param}')

	def get_audio(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:AUDio \n
		Snippet: value: bool = driver.source.afRf.generator.voip.get_audio() \n
		Enables or disables feeding an audio signal into the VoIP path. \n
			:return: af_2_vo_ip_enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:AUDio?')
		return Conversions.str_to_bool(response)

	def set_audio(self, af_2_vo_ip_enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:AUDio \n
		Snippet: driver.source.afRf.generator.voip.set_audio(af_2_vo_ip_enable = False) \n
		Enables or disables feeding an audio signal into the VoIP path. \n
			:param af_2_vo_ip_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(af_2_vo_ip_enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:VOIP:AUDio {param}')

	def get_fid(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:FID \n
		Snippet: value: float = driver.source.afRf.generator.voip.get_fid() \n
		Specifies the frequency ID (FID) configured at the DUT.
			INTRO_CMD_HELP: Allowed values are, with n = 0 to 39995: \n
			- 0.100 + n * 0.025
			- 0.105 + n * 0.025
			- 0.110 + n * 0.025
			- 0.115 + n * 0.025
		Resulting in: 0.100, 0.105, 0.110, 0.115, 0.125, 0.130, 0.135, 0.140, ..., 999.975, 999.980, 999.985, 999.990 \n
			:return: freq_id: Frequency ID Not allowed values are rounded to the closest allowed value. Range: 0.1 to 999.99
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:FID?')
		return Conversions.str_to_float(response)

	def set_fid(self, freq_id: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:FID \n
		Snippet: driver.source.afRf.generator.voip.set_fid(freq_id = 1.0) \n
		Specifies the frequency ID (FID) configured at the DUT.
			INTRO_CMD_HELP: Allowed values are, with n = 0 to 39995: \n
			- 0.100 + n * 0.025
			- 0.105 + n * 0.025
			- 0.110 + n * 0.025
			- 0.115 + n * 0.025
		Resulting in: 0.100, 0.105, 0.110, 0.115, 0.125, 0.130, 0.135, 0.140, ..., 999.975, 999.980, 999.985, 999.990 \n
			:param freq_id: Frequency ID Not allowed values are rounded to the closest allowed value. Range: 0.1 to 999.99
		"""
		param = Conversions.decimal_value_to_str(freq_id)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:VOIP:FID {param}')

	# noinspection PyTypeChecker
	class FrequencyStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Freq: float: RF carrier center frequency Unit: Hz
			- Chanspac: int: Channel spacing Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Freq'),
			ArgStruct.scalar_int('Chanspac')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Freq: float = None
			self.Chanspac: int = None

	def get_frequency(self) -> FrequencyStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:FREQuency \n
		Snippet: value: FrequencyStruct = driver.source.afRf.generator.voip.get_frequency() \n
		Queries the RF carrier center frequency and the channel spacing resulting from the configured frequency ID. \n
			:return: structure: for return value, see the help for FrequencyStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:AFRF:GENerator<Instance>:VOIP:FREQuency?', self.__class__.FrequencyStruct())

	# noinspection PyTypeChecker
	def get_value(self) -> enums.VoIpSource:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP \n
		Snippet: value: enums.VoIpSource = driver.source.afRf.generator.voip.get_value() \n
		Selects an audio signal source for the VoIP path. \n
			:return: vo_ip_source: GEN4 | AFI1 | AFI2 GEN4 Audio generator 4
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP?')
		return Conversions.str_to_scalar_enum(response, enums.VoIpSource)

	def set_value(self, vo_ip_source: enums.VoIpSource) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP \n
		Snippet: driver.source.afRf.generator.voip.set_value(vo_ip_source = enums.VoIpSource.AFI1) \n
		Selects an audio signal source for the VoIP path. \n
			:param vo_ip_source: GEN4 | AFI1 | AFI2 GEN4 Audio generator 4
		"""
		param = Conversions.enum_scalar_to_str(vo_ip_source, enums.VoIpSource)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:VOIP {param}')

	def clone(self) -> 'Voip':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Voip(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
