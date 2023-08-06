from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Subtone:
	"""Subtone commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subtone", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:SUBTone:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.tones.subtone.get_enable() \n
		Enables or disables the subtone. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:SUBTone:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:SUBTone:ENABle \n
		Snippet: driver.source.afRf.generator.tones.subtone.set_enable(enable = False) \n
		Enables or disables the subtone. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:SUBTone:ENABle {param}')

	def get_frequency(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:SUBTone:FREQuency \n
		Snippet: value: float = driver.source.afRf.generator.tones.subtone.get_frequency() \n
		Specifies the frequency of a generated subtone. \n
			:return: frequency: Range: 0 Hz to 2000 Hz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:SUBTone:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:SUBTone:FREQuency \n
		Snippet: driver.source.afRf.generator.tones.subtone.set_frequency(frequency = 1.0) \n
		Specifies the frequency of a generated subtone. \n
			:param frequency: Range: 0 Hz to 2000 Hz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:SUBTone:FREQuency {param}')
