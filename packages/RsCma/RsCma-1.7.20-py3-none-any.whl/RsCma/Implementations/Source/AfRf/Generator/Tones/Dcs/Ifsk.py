from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ifsk:
	"""Ifsk commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ifsk", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:IFSK:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.tones.dcs.ifsk.get_enable() \n
		Enables or disables the inversion of the FSK modulation polarity. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:DCS:IFSK:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:IFSK:ENABle \n
		Snippet: driver.source.afRf.generator.tones.dcs.ifsk.set_enable(enable = False) \n
		Enables or disables the inversion of the FSK modulation polarity. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:DCS:IFSK:ENABle {param}')
