from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Af:
	"""Af commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("af", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:AF:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.interferer.af.get_enable() \n
		Enables or disables a single tone. If the tone is disabled, the interferer is unmodulated, even if a modulation mode has
		been configured. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:IFERer:AF:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:AF:ENABle \n
		Snippet: driver.source.afRf.generator.interferer.af.set_enable(enable = False) \n
		Enables or disables a single tone. If the tone is disabled, the interferer is unmodulated, even if a modulation mode has
		been configured. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IFERer:AF:ENABle {param}')

	def get_frequency(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:AF:FREQuency \n
		Snippet: value: float = driver.source.afRf.generator.interferer.af.get_frequency() \n
		Configures the frequency of a single tone, that can be added to the interferer. \n
			:return: frequency: Range: 0 Hz to 21 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:IFERer:AF:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:AF:FREQuency \n
		Snippet: driver.source.afRf.generator.interferer.af.set_frequency(frequency = 1.0) \n
		Configures the frequency of a single tone, that can be added to the interferer. \n
			:param frequency: Range: 0 Hz to 21 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IFERer:AF:FREQuency {param}')
