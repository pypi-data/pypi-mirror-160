from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rf:
	"""Rf commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rf", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIGital:RF:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.digital.rf.get_enable() \n
		No command help available \n
			:return: dig_rf_enable: No help available
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIGital:RF:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, dig_rf_enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIGital:RF:ENABle \n
		Snippet: driver.source.afRf.generator.digital.rf.set_enable(dig_rf_enable = False) \n
		No command help available \n
			:param dig_rf_enable: No help available
		"""
		param = Conversions.bool_to_str(dig_rf_enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIGital:RF:ENABle {param}')
