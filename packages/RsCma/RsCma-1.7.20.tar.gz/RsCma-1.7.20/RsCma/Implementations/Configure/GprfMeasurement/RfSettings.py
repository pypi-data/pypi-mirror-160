from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfSettings:
	"""RfSettings commands group definition. 5 total commands, 0 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rfSettings", core, parent)

	# noinspection PyTypeChecker
	def get_connector(self) -> enums.InputConnector:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:RFSettings:CONNector \n
		Snippet: value: enums.InputConnector = driver.configure.gprfMeasurement.rfSettings.get_connector() \n
		Selects the input connector for the measured RF signal. \n
			:return: input_connector: RFCom | RFIN
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:RFSettings:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.InputConnector)

	def set_connector(self, input_connector: enums.InputConnector) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:RFSettings:CONNector \n
		Snippet: driver.configure.gprfMeasurement.rfSettings.set_connector(input_connector = enums.InputConnector.RFCom) \n
		Selects the input connector for the measured RF signal. \n
			:param input_connector: RFCom | RFIN
		"""
		param = Conversions.enum_scalar_to_str(input_connector, enums.InputConnector)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:RFSettings:CONNector {param}')

	def get_frequency(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:RFSettings:FREQuency \n
		Snippet: value: float = driver.configure.gprfMeasurement.rfSettings.get_frequency() \n
		Sets the center frequency of the RF analyzer. \n
			:return: analyzer_freq: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:RFSettings:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, analyzer_freq: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:RFSettings:FREQuency \n
		Snippet: driver.configure.gprfMeasurement.rfSettings.set_frequency(analyzer_freq = 1.0) \n
		Sets the center frequency of the RF analyzer. \n
			:param analyzer_freq: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(analyzer_freq)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:RFSettings:FREQuency {param}')

	def get_envelope_power(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:RFSettings:ENPower \n
		Snippet: value: float = driver.configure.gprfMeasurement.rfSettings.get_envelope_power() \n
		Sets the expected nominal power of the measured RF signal. The allowed range depends on several other settings, for
		example on the selected connector and the external attenuation. For supported ranges, refer to the data sheet. \n
			:return: exp_nominal_power: Unit: dBm
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:RFSettings:ENPower?')
		return Conversions.str_to_float(response)

	def set_envelope_power(self, exp_nominal_power: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:RFSettings:ENPower \n
		Snippet: driver.configure.gprfMeasurement.rfSettings.set_envelope_power(exp_nominal_power = 1.0) \n
		Sets the expected nominal power of the measured RF signal. The allowed range depends on several other settings, for
		example on the selected connector and the external attenuation. For supported ranges, refer to the data sheet. \n
			:param exp_nominal_power: Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(exp_nominal_power)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:RFSettings:ENPower {param}')

	def get_eattenuation(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:RFSettings:EATTenuation \n
		Snippet: value: float = driver.configure.gprfMeasurement.rfSettings.get_eattenuation() \n
		Specifies the external attenuation in the input path. Negative values specify a gain. \n
			:return: rf_input_ext_att: Range: -50 dB to 90 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:RFSettings:EATTenuation?')
		return Conversions.str_to_float(response)

	def set_eattenuation(self, rf_input_ext_att: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:RFSettings:EATTenuation \n
		Snippet: driver.configure.gprfMeasurement.rfSettings.set_eattenuation(rf_input_ext_att = 1.0) \n
		Specifies the external attenuation in the input path. Negative values specify a gain. \n
			:param rf_input_ext_att: Range: -50 dB to 90 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(rf_input_ext_att)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:RFSettings:EATTenuation {param}')

	def get_rf_coupling(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:RFSettings:RFCoupling \n
		Snippet: value: bool = driver.configure.gprfMeasurement.rfSettings.get_rf_coupling() \n
		Couples the frequency setting of the measurement to the corresponding generator setting. \n
			:return: rf_coupling: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:RFSettings:RFCoupling?')
		return Conversions.str_to_bool(response)

	def set_rf_coupling(self, rf_coupling: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:RFSettings:RFCoupling \n
		Snippet: driver.configure.gprfMeasurement.rfSettings.set_rf_coupling(rf_coupling = False) \n
		Couples the frequency setting of the measurement to the corresponding generator setting. \n
			:param rf_coupling: OFF | ON
		"""
		param = Conversions.bool_to_str(rf_coupling)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:RFSettings:RFCoupling {param}')
