from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfSettings:
	"""RfSettings commands group definition. 10 total commands, 2 Subgroups, 8 group commands"""

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

	# noinspection PyTypeChecker
	def get_connector(self) -> enums.InputConnector:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:CONNector \n
		Snippet: value: enums.InputConnector = driver.configure.afRf.measurement.rfSettings.get_connector() \n
		Selects the input connector for the measured RF signal. \n
			:return: input_connector: RFCom | RFIN
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:RFSettings:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.InputConnector)

	def set_connector(self, input_connector: enums.InputConnector) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:CONNector \n
		Snippet: driver.configure.afRf.measurement.rfSettings.set_connector(input_connector = enums.InputConnector.RFCom) \n
		Selects the input connector for the measured RF signal. \n
			:param input_connector: RFCom | RFIN
		"""
		param = Conversions.enum_scalar_to_str(input_connector, enums.InputConnector)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:CONNector {param}')

	def get_frequency(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:FREQuency \n
		Snippet: value: float = driver.configure.afRf.measurement.rfSettings.get_frequency() \n
		Sets the center frequency of the RF analyzer. \n
			:return: frequency: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:RFSettings:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:FREQuency \n
		Snippet: driver.configure.afRf.measurement.rfSettings.set_frequency(frequency = 1.0) \n
		Sets the center frequency of the RF analyzer. \n
			:param frequency: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:FREQuency {param}')

	def get_envelope_power(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:ENPower \n
		Snippet: value: float = driver.configure.afRf.measurement.rfSettings.get_envelope_power() \n
		Sets the expected nominal power of the measured RF signal. The allowed range depends on several other settings, for
		example on the selected connector and the external attenuation. For supported ranges, refer to the data sheet. \n
			:return: exp_nominal_power: Unit: dBm
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:RFSettings:ENPower?')
		return Conversions.str_to_float(response)

	def set_envelope_power(self, exp_nominal_power: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:ENPower \n
		Snippet: driver.configure.afRf.measurement.rfSettings.set_envelope_power(exp_nominal_power = 1.0) \n
		Sets the expected nominal power of the measured RF signal. The allowed range depends on several other settings, for
		example on the selected connector and the external attenuation. For supported ranges, refer to the data sheet. \n
			:param exp_nominal_power: Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(exp_nominal_power)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:ENPower {param}')

	def get_eattenuation(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:EATTenuation \n
		Snippet: value: float = driver.configure.afRf.measurement.rfSettings.get_eattenuation() \n
		Specifies the external attenuation in the input path. Negative values specify a gain. \n
			:return: rf_input_ext_att: Range: -50 dB to 90 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:RFSettings:EATTenuation?')
		return Conversions.str_to_float(response)

	def set_eattenuation(self, rf_input_ext_att: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:EATTenuation \n
		Snippet: driver.configure.afRf.measurement.rfSettings.set_eattenuation(rf_input_ext_att = 1.0) \n
		Specifies the external attenuation in the input path. Negative values specify a gain. \n
			:param rf_input_ext_att: Range: -50 dB to 90 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(rf_input_ext_att)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:EATTenuation {param}')

	def get_rf_coupling(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:RFCoupling \n
		Snippet: value: bool = driver.configure.afRf.measurement.rfSettings.get_rf_coupling() \n
		Couples the frequency and channel settings of the analyzer to the corresponding generator settings. \n
			:return: rf_coupling: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:RFSettings:RFCoupling?')
		return Conversions.str_to_bool(response)

	def set_rf_coupling(self, rf_coupling: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:RFCoupling \n
		Snippet: driver.configure.afRf.measurement.rfSettings.set_rf_coupling(rf_coupling = False) \n
		Couples the frequency and channel settings of the analyzer to the corresponding generator settings. \n
			:param rf_coupling: OFF | ON
		"""
		param = Conversions.bool_to_str(rf_coupling)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:RFCoupling {param}')

	def get_dspace(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:DSPace \n
		Snippet: value: float = driver.configure.afRf.measurement.rfSettings.get_dspace() \n
		Configures the duplex spacing between the analyzer frequency and the generator frequency.
		Frequencyanalyzer = frequencygenerator + duplex spacing This command is only relevant with enabled RF coupling. \n
			:return: duplex_space: Range: -500 MHz to 500 MHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:RFSettings:DSPace?')
		return Conversions.str_to_float(response)

	def set_dspace(self, duplex_space: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:DSPace \n
		Snippet: driver.configure.afRf.measurement.rfSettings.set_dspace(duplex_space = 1.0) \n
		Configures the duplex spacing between the analyzer frequency and the generator frequency.
		Frequencyanalyzer = frequencygenerator + duplex spacing This command is only relevant with enabled RF coupling. \n
			:param duplex_space: Range: -500 MHz to 500 MHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(duplex_space)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:DSPace {param}')

	def get_channel(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:CHANnel \n
		Snippet: value: int = driver.configure.afRf.measurement.rfSettings.get_channel() \n
		Specifies the center frequency of the RF analyzer via a channel number, according to the configured channel definition. \n
			:return: rf_channel: Range: 0 Ch to 9999 Ch, Unit: Ch
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:RFSettings:CHANnel?')
		return Conversions.str_to_int(response)

	def set_channel(self, rf_channel: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:CHANnel \n
		Snippet: driver.configure.afRf.measurement.rfSettings.set_channel(rf_channel = 1) \n
		Specifies the center frequency of the RF analyzer via a channel number, according to the configured channel definition. \n
			:param rf_channel: Range: 0 Ch to 9999 Ch, Unit: Ch
		"""
		param = Conversions.decimal_value_to_str(rf_channel)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:CHANnel {param}')

	def get_coffset(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:COFFset \n
		Snippet: value: float = driver.configure.afRf.measurement.rfSettings.get_coffset() \n
		Shifts the center frequency of the RF analyzer by a channel offset, relative to the frequency defined via the channel
		number. The range depends on the channel spacing, defined via method RsCma.Configure.AfRf.Measurement.Cdefinition.cspace. \n
			:return: channel_offset: Range: -Spacing/2 Hz to +Spacing/2 Hz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:RFSettings:COFFset?')
		return Conversions.str_to_float(response)

	def set_coffset(self, channel_offset: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:COFFset \n
		Snippet: driver.configure.afRf.measurement.rfSettings.set_coffset(channel_offset = 1.0) \n
		Shifts the center frequency of the RF analyzer by a channel offset, relative to the frequency defined via the channel
		number. The range depends on the channel spacing, defined via method RsCma.Configure.AfRf.Measurement.Cdefinition.cspace. \n
			:param channel_offset: Range: -Spacing/2 Hz to +Spacing/2 Hz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(channel_offset)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:COFFset {param}')

	def clone(self) -> 'RfSettings':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfSettings(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
