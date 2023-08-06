from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reference:
	"""Reference commands group definition. 6 total commands, 1 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reference", core, parent)

	@property
	def fdeviation(self):
		"""fdeviation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._cmd_group)
		return self._fdeviation

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:ENABle \n
		Snippet: value: bool = driver.source.avionics.generator.vor.afSettings.reference.get_enable() \n
		Enables or disables the REF signal. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:ENABle \n
		Snippet: driver.source.avionics.generator.vor.afSettings.reference.set_enable(enable = False) \n
		Enables or disables the REF signal. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:ENABle {param}')

	def get_mod_depth(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:MDEPth \n
		Snippet: value: float = driver.source.avionics.generator.vor.afSettings.reference.get_mod_depth() \n
		Sets the AM modulation depth of the FM subcarrier. The sum of the modulation depths for all enabled components must not
		exceed 100 %. \n
			:return: vor_mod_depth: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:MDEPth?')
		return Conversions.str_to_float(response)

	def set_mod_depth(self, vor_mod_depth: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:MDEPth \n
		Snippet: driver.source.avionics.generator.vor.afSettings.reference.set_mod_depth(vor_mod_depth = 1.0) \n
		Sets the AM modulation depth of the FM subcarrier. The sum of the modulation depths for all enabled components must not
		exceed 100 %. \n
			:param vor_mod_depth: Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(vor_mod_depth)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:MDEPth {param}')

	def get_cfrequency(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:CFRequency \n
		Snippet: value: float = driver.source.avionics.generator.vor.afSettings.reference.get_cfrequency() \n
		Sets the center frequency of the FM subcarrier. \n
			:return: freq: Range: 7500 Hz to 12.5 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:CFRequency?')
		return Conversions.str_to_float(response)

	def set_cfrequency(self, freq: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:CFRequency \n
		Snippet: driver.source.avionics.generator.vor.afSettings.reference.set_cfrequency(freq = 1.0) \n
		Sets the center frequency of the FM subcarrier. \n
			:param freq: Range: 7500 Hz to 12.5 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(freq)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:CFRequency {param}')

	def get_frequency(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FREQuency \n
		Snippet: value: float = driver.source.avionics.generator.vor.afSettings.reference.get_frequency() \n
		Sets the audio frequency of the REF signal and the VAR signal. \n
			:return: freq: Range: 20 Hz to 40 Hz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, freq: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FREQuency \n
		Snippet: driver.source.avionics.generator.vor.afSettings.reference.set_frequency(freq = 1.0) \n
		Sets the audio frequency of the REF signal and the VAR signal. \n
			:param freq: Range: 20 Hz to 40 Hz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(freq)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FREQuency {param}')

	def clone(self) -> 'Reference':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Reference(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
