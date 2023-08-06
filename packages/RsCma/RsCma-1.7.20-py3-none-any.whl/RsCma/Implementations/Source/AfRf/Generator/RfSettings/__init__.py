from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfSettings:
	"""RfSettings commands group definition. 11 total commands, 2 Subgroups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rfSettings", core, parent)

	@property
	def rf(self):
		"""rf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import Rf
			self._rf = Rf(self._core, self._cmd_group)
		return self._rf

	@property
	def farFrequency(self):
		"""farFrequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_farFrequency'):
			from .FarFrequency import FarFrequency
			self._farFrequency = FarFrequency(self._core, self._cmd_group)
		return self._farFrequency

	def get_dgain(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:DGAin \n
		Snippet: value: float = driver.source.afRf.generator.rfSettings.get_dgain() \n
		Specifies a digital gain and thus modifies the configured RMS base level by a specific value. \n
			:return: dig_gain: Range: -30 dB to 0 dB, Unit: dB
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:RFSettings:DGAin?')
		return Conversions.str_to_float(response)

	def set_dgain(self, dig_gain: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:DGAin \n
		Snippet: driver.source.afRf.generator.rfSettings.set_dgain(dig_gain = 1.0) \n
		Specifies a digital gain and thus modifies the configured RMS base level by a specific value. \n
			:param dig_gain: Range: -30 dB to 0 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(dig_gain)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:RFSettings:DGAin {param}')

	def get_eattenuation(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:EATTenuation \n
		Snippet: value: float = driver.source.afRf.generator.rfSettings.get_eattenuation() \n
		Specifies the external attenuation in the RF output path. Negative values specify a gain. \n
			:return: rf_output_ext_att: Range: -50 dB to 90 dB, Unit: dB
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:RFSettings:EATTenuation?')
		return Conversions.str_to_float(response)

	def set_eattenuation(self, rf_output_ext_att: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:EATTenuation \n
		Snippet: driver.source.afRf.generator.rfSettings.set_eattenuation(rf_output_ext_att = 1.0) \n
		Specifies the external attenuation in the RF output path. Negative values specify a gain. \n
			:param rf_output_ext_att: Range: -50 dB to 90 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(rf_output_ext_att)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:RFSettings:EATTenuation {param}')

	def get_frequency(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:FREQuency \n
		Snippet: value: float = driver.source.afRf.generator.rfSettings.get_frequency() \n
		Specifies the center frequency of the unmodulated RF carrier. \n
			:return: frequency: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:RFSettings:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:FREQuency \n
		Snippet: driver.source.afRf.generator.rfSettings.set_frequency(frequency = 1.0) \n
		Specifies the center frequency of the unmodulated RF carrier. \n
			:param frequency: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:RFSettings:FREQuency {param}')

	def get_level(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:LEVel \n
		Snippet: value: float = driver.source.afRf.generator.rfSettings.get_level() \n
		Specifies the RMS level of the unmodulated RF signal. The allowed range depends on several other settings, for example on
		the selected connector, the frequency and the external attenuation. For supported output level ranges, refer to the data
		sheet. \n
			:return: level: Unit: dBm
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:RFSettings:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:LEVel \n
		Snippet: driver.source.afRf.generator.rfSettings.set_level(level = 1.0) \n
		Specifies the RMS level of the unmodulated RF signal. The allowed range depends on several other settings, for example on
		the selected connector, the frequency and the external attenuation. For supported output level ranges, refer to the data
		sheet. \n
			:param level: Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:RFSettings:LEVel {param}')

	def get_pe_power(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:PEPower \n
		Snippet: value: float = driver.source.afRf.generator.rfSettings.get_pe_power() \n
		Queries the peak envelope power (PEP) . \n
			:return: peak_envelope_power: Unit: dBm
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:RFSettings:PEPower?')
		return Conversions.str_to_float(response)

	def get_rf_coupling(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:RFCoupling \n
		Snippet: value: bool = driver.source.afRf.generator.rfSettings.get_rf_coupling() \n
		No command help available \n
			:return: enable: No help available
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:RFSettings:RFCoupling?')
		return Conversions.str_to_bool(response)

	def set_rf_coupling(self, enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:RFCoupling \n
		Snippet: driver.source.afRf.generator.rfSettings.set_rf_coupling(enable = False) \n
		No command help available \n
			:param enable: No help available
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:RFSettings:RFCoupling {param}')

	# noinspection PyTypeChecker
	def get_connector(self) -> enums.OutputConnector:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:CONNector \n
		Snippet: value: enums.OutputConnector = driver.source.afRf.generator.rfSettings.get_connector() \n
		Selects the output connector for the generated RF signal. \n
			:return: output_connector: RFCom | RFOut
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:RFSettings:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.OutputConnector)

	def set_connector(self, output_connector: enums.OutputConnector) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:CONNector \n
		Snippet: driver.source.afRf.generator.rfSettings.set_connector(output_connector = enums.OutputConnector.RFCom) \n
		Selects the output connector for the generated RF signal. \n
			:param output_connector: RFCom | RFOut
		"""
		param = Conversions.enum_scalar_to_str(output_connector, enums.OutputConnector)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:RFSettings:CONNector {param}')

	def get_channel(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:CHANnel \n
		Snippet: value: int = driver.source.afRf.generator.rfSettings.get_channel() \n
		Specifies the center frequency of the unmodulated RF carrier via a channel number, according to the configured channel
		definition. \n
			:return: channel: Range: 0 Ch to 9999 Ch, Unit: Ch
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:RFSettings:CHANnel?')
		return Conversions.str_to_int(response)

	def set_channel(self, channel: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:CHANnel \n
		Snippet: driver.source.afRf.generator.rfSettings.set_channel(channel = 1) \n
		Specifies the center frequency of the unmodulated RF carrier via a channel number, according to the configured channel
		definition. \n
			:param channel: Range: 0 Ch to 9999 Ch, Unit: Ch
		"""
		param = Conversions.decimal_value_to_str(channel)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:RFSettings:CHANnel {param}')

	def get_coffset(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:COFFset \n
		Snippet: value: float = driver.source.afRf.generator.rfSettings.get_coffset() \n
		Shifts the center frequency of the unmodulated RF carrier by a channel offset, relative to the frequency defined via the
		channel number. The range depends on the channel spacing, defined via method RsCma.Source.AfRf.Generator.Cdefinition.
		cspace. \n
			:return: channel_offset: Range: -Spacing/2 Hz to +Spacing/2 Hz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:RFSettings:COFFset?')
		return Conversions.str_to_float(response)

	def set_coffset(self, channel_offset: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:COFFset \n
		Snippet: driver.source.afRf.generator.rfSettings.set_coffset(channel_offset = 1.0) \n
		Shifts the center frequency of the unmodulated RF carrier by a channel offset, relative to the frequency defined via the
		channel number. The range depends on the channel spacing, defined via method RsCma.Source.AfRf.Generator.Cdefinition.
		cspace. \n
			:param channel_offset: Range: -Spacing/2 Hz to +Spacing/2 Hz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(channel_offset)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:RFSettings:COFFset {param}')

	def clone(self) -> 'RfSettings':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfSettings(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
