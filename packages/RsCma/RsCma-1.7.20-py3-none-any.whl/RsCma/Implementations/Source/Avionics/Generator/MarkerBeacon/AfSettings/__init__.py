from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AfSettings:
	"""AfSettings commands group definition. 6 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("afSettings", core, parent)

	@property
	def audioOutput(self):
		"""audioOutput commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_audioOutput'):
			from .AudioOutput import AudioOutput
			self._audioOutput = AudioOutput(self._core, self._cmd_group)
		return self._audioOutput

	# noinspection PyTypeChecker
	def get_connector(self) -> enums.AudioConnector:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:CONNector \n
		Snippet: value: enums.AudioConnector = driver.source.avionics.generator.markerBeacon.afSettings.get_connector() \n
		Selects the output connector for the generated AF signal (AF1 OUT or AF2 OUT) . \n
			:return: connector: AF1O | AF2O
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.AudioConnector)

	def set_connector(self, connector: enums.AudioConnector) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:CONNector \n
		Snippet: driver.source.avionics.generator.markerBeacon.afSettings.set_connector(connector = enums.AudioConnector.AF1O) \n
		Selects the output connector for the generated AF signal (AF1 OUT or AF2 OUT) . \n
			:param connector: AF1O | AF2O
		"""
		param = Conversions.enum_scalar_to_str(connector, enums.AudioConnector)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:CONNector {param}')

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:ENABle \n
		Snippet: value: bool = driver.source.avionics.generator.markerBeacon.afSettings.get_enable() \n
		Enables or disables the modulation of the RF carrier with the marker beacon audio tone. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:ENABle \n
		Snippet: driver.source.avionics.generator.markerBeacon.afSettings.set_enable(enable = False) \n
		Enables or disables the modulation of the RF carrier with the marker beacon audio tone. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:ENABle {param}')

	def get_mod_depth(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:MDEPth \n
		Snippet: value: float = driver.source.avionics.generator.markerBeacon.afSettings.get_mod_depth() \n
		Sets the modulation depth for amplitude modulation of the carrier. The sum of the modulation depths for all enabled
		components must not exceed 100 %. \n
			:return: mod_depth: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:MDEPth?')
		return Conversions.str_to_float(response)

	def set_mod_depth(self, mod_depth: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:MDEPth \n
		Snippet: driver.source.avionics.generator.markerBeacon.afSettings.set_mod_depth(mod_depth = 1.0) \n
		Sets the modulation depth for amplitude modulation of the carrier. The sum of the modulation depths for all enabled
		components must not exceed 100 %. \n
			:param mod_depth: Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(mod_depth)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:MDEPth {param}')

	def get_frequency(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:FREQuency \n
		Snippet: value: float = driver.source.avionics.generator.markerBeacon.afSettings.get_frequency() \n
		Sets the audio frequency of the tone to be modulated to the carrier. \n
			:return: freq: Range: 0 Hz to 10 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, freq: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:FREQuency \n
		Snippet: driver.source.avionics.generator.markerBeacon.afSettings.set_frequency(freq = 1.0) \n
		Sets the audio frequency of the tone to be modulated to the carrier. \n
			:param freq: Range: 0 Hz to 10 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(freq)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:FREQuency {param}')

	def clone(self) -> 'AfSettings':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AfSettings(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
