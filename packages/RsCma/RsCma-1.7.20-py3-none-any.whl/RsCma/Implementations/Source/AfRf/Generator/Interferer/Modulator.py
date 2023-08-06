from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulator:
	"""Modulator commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("modulator", core, parent)

	def get_fdeviation(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:FDEViation \n
		Snippet: value: float = driver.source.afRf.generator.interferer.modulator.get_fdeviation() \n
		Specifies the maximum frequency deviation for the FM interferer mode. \n
			:return: freq_deviation: Range: 0 Hz to 100 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:FDEViation?')
		return Conversions.str_to_float(response)

	def set_fdeviation(self, freq_deviation: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:FDEViation \n
		Snippet: driver.source.afRf.generator.interferer.modulator.set_fdeviation(freq_deviation = 1.0) \n
		Specifies the maximum frequency deviation for the FM interferer mode. \n
			:param freq_deviation: Range: 0 Hz to 100 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(freq_deviation)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:FDEViation {param}')

	def get_pdeviation(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:PDEViation \n
		Snippet: value: float = driver.source.afRf.generator.interferer.modulator.get_pdeviation() \n
		Specifies the maximum phase deviation for the PM interferer mode. \n
			:return: phase_deviation: Range: 0 rad to 10 rad, Unit: rad
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:PDEViation?')
		return Conversions.str_to_float(response)

	def set_pdeviation(self, phase_deviation: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:PDEViation \n
		Snippet: driver.source.afRf.generator.interferer.modulator.set_pdeviation(phase_deviation = 1.0) \n
		Specifies the maximum phase deviation for the PM interferer mode. \n
			:param phase_deviation: Range: 0 rad to 10 rad, Unit: rad
		"""
		param = Conversions.decimal_value_to_str(phase_deviation)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:PDEViation {param}')

	def get_mod_depth(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:MDEPth \n
		Snippet: value: float = driver.source.afRf.generator.interferer.modulator.get_mod_depth() \n
		Specifies the modulation depth for the AM interferer mode. \n
			:return: modulation_depth: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:MDEPth?')
		return Conversions.str_to_float(response)

	def set_mod_depth(self, modulation_depth: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:MDEPth \n
		Snippet: driver.source.afRf.generator.interferer.modulator.set_mod_depth(modulation_depth = 1.0) \n
		Specifies the modulation depth for the AM interferer mode. \n
			:param modulation_depth: Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(modulation_depth)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IFERer:MODulator:MDEPth {param}')
