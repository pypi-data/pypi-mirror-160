from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfSettings:
	"""RfSettings commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rfSettings", core, parent)

	# noinspection PyTypeChecker
	def get_connector(self) -> enums.OutputConnector:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:RFSettings:CONNector \n
		Snippet: value: enums.OutputConnector = driver.source.avionics.generator.rfSettings.get_connector() \n
		Selects the output connector for the generated RF signal. \n
			:return: connector: RFCom | RFOut
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:RFSettings:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.OutputConnector)

	def set_connector(self, connector: enums.OutputConnector) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:RFSettings:CONNector \n
		Snippet: driver.source.avionics.generator.rfSettings.set_connector(connector = enums.OutputConnector.RFCom) \n
		Selects the output connector for the generated RF signal. \n
			:param connector: RFCom | RFOut
		"""
		param = Conversions.enum_scalar_to_str(connector, enums.OutputConnector)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:RFSettings:CONNector {param}')

	def get_eattenuation(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:RFSettings:EATTenuation \n
		Snippet: value: float = driver.source.avionics.generator.rfSettings.get_eattenuation() \n
		Specifies the external attenuation in the RF output path. Negative values specify a gain. \n
			:return: ext_atten: Range: -50 dB to 90 dB, Unit: dB
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:RFSettings:EATTenuation?')
		return Conversions.str_to_float(response)

	def set_eattenuation(self, ext_atten: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:RFSettings:EATTenuation \n
		Snippet: driver.source.avionics.generator.rfSettings.set_eattenuation(ext_atten = 1.0) \n
		Specifies the external attenuation in the RF output path. Negative values specify a gain. \n
			:param ext_atten: Range: -50 dB to 90 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(ext_atten)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:RFSettings:EATTenuation {param}')
