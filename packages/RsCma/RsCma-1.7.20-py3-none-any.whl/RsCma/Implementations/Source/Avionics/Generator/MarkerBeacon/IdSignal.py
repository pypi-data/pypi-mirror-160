from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IdSignal:
	"""IdSignal commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("idSignal", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:ENABle \n
		Snippet: value: bool = driver.source.avionics.generator.markerBeacon.idSignal.get_enable() \n
		Enables or disables the ID signal. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:ENABle \n
		Snippet: driver.source.avionics.generator.markerBeacon.idSignal.set_enable(enable = False) \n
		Enables or disables the ID signal. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:ENABle {param}')

	def get_mod_depth(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:MDEPth \n
		Snippet: value: float = driver.source.avionics.generator.markerBeacon.idSignal.get_mod_depth() \n
		Configures the modulation depth for the ID signal. The sum of the modulation depths for all enabled components must not
		exceed 100 %. \n
			:return: mod_depth: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:MDEPth?')
		return Conversions.str_to_float(response)

	def set_mod_depth(self, mod_depth: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:MDEPth \n
		Snippet: driver.source.avionics.generator.markerBeacon.idSignal.set_mod_depth(mod_depth = 1.0) \n
		Configures the modulation depth for the ID signal. The sum of the modulation depths for all enabled components must not
		exceed 100 %. \n
			:param mod_depth: Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(mod_depth)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:MDEPth {param}')

	def get_frequency(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:FREQuency \n
		Snippet: value: float = driver.source.avionics.generator.markerBeacon.idSignal.get_frequency() \n
		Configures the frequency of the ID signal. \n
			:return: freq: Range: 0 Hz to 21 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, freq: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:FREQuency \n
		Snippet: driver.source.avionics.generator.markerBeacon.idSignal.set_frequency(freq = 1.0) \n
		Configures the frequency of the ID signal. \n
			:param freq: Range: 0 Hz to 21 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(freq)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:MBEacon:IDSignal:FREQuency {param}')
