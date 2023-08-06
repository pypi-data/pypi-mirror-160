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
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:RF:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.rfSettings.rf.get_enable() \n
		Enables or disables the RF signal, without changing the generator state. \n
			:return: rf_enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:RFSettings:RF:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, rf_enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RFSettings:RF:ENABle \n
		Snippet: driver.source.afRf.generator.rfSettings.rf.set_enable(rf_enable = False) \n
		Enables or disables the RF signal, without changing the generator state. \n
			:param rf_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(rf_enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:RFSettings:RF:ENABle {param}')
