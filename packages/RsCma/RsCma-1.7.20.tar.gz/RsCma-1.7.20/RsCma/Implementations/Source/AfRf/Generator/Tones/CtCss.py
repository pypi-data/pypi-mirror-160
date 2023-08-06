from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CtCss:
	"""CtCss commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ctCss", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:CTCSs:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.tones.ctCss.get_enable() \n
		Enables or disables the CTCSS tone. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:CTCSs:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:CTCSs:ENABle \n
		Snippet: driver.source.afRf.generator.tones.ctCss.set_enable(enable = False) \n
		Enables or disables the CTCSS tone. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:CTCSs:ENABle {param}')

	def get_tnumber(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:CTCSs:TNUMber \n
		Snippet: value: int = driver.source.afRf.generator.tones.ctCss.get_tnumber() \n
		Selects a CTCSS tone via its number in the tone list. \n
			:return: tone_number: Range: 1 to 50
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:CTCSs:TNUMber?')
		return Conversions.str_to_int(response)

	def set_tnumber(self, tone_number: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:CTCSs:TNUMber \n
		Snippet: driver.source.afRf.generator.tones.ctCss.set_tnumber(tone_number = 1) \n
		Selects a CTCSS tone via its number in the tone list. \n
			:param tone_number: Range: 1 to 50
		"""
		param = Conversions.decimal_value_to_str(tone_number)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:CTCSs:TNUMber {param}')
