from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fdeviation:
	"""Fdeviation commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdeviation", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FDEViation:ENABle \n
		Snippet: value: bool = driver.source.avionics.generator.vor.afSettings.reference.fdeviation.get_enable() \n
		Enables or disables the modulation of the FM subcarrier with the REF signal. \n
			:return: vor_freq_deviation: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FDEViation:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, vor_freq_deviation: bool) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FDEViation:ENABle \n
		Snippet: driver.source.avionics.generator.vor.afSettings.reference.fdeviation.set_enable(vor_freq_deviation = False) \n
		Enables or disables the modulation of the FM subcarrier with the REF signal. \n
			:param vor_freq_deviation: OFF | ON
		"""
		param = Conversions.bool_to_str(vor_freq_deviation)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FDEViation:ENABle {param}')

	def get_value(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FDEViation \n
		Snippet: value: float = driver.source.avionics.generator.vor.afSettings.reference.fdeviation.get_value() \n
		Sets the frequency deviation of the REF signal on the FM subcarrier. \n
			:return: vor_freq_deviation: Range: 300 Hz to 600 Hz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FDEViation?')
		return Conversions.str_to_float(response)

	def set_value(self, vor_freq_deviation: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FDEViation \n
		Snippet: driver.source.avionics.generator.vor.afSettings.reference.fdeviation.set_value(vor_freq_deviation = 1.0) \n
		Sets the frequency deviation of the REF signal on the FM subcarrier. \n
			:param vor_freq_deviation: Range: 300 Hz to 600 Hz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(vor_freq_deviation)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:REFerence:FDEViation {param}')
