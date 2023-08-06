from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, tone_status: List[bool], internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:ENABle \n
		Snippet: driver.source.afRf.generator.internalGenerator.multiTone.enable.set(tone_status = [True, False, True], internalGen = repcap.InternalGen.Default) \n
		Enables or disables the tone list entries for multitone generation. \n
			:param tone_status: OFF | ON Comma-separated list of up to 20 values, tone 1 to tone 20 You can specify fewer than 20 values to configure only the beginning of the tone list.
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
		"""
		param = Conversions.list_to_csv_str(tone_status)
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:ENABle {param}')

	def get(self, internalGen=repcap.InternalGen.Default) -> List[bool]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:ENABle \n
		Snippet: value: List[bool] = driver.source.afRf.generator.internalGenerator.multiTone.enable.get(internalGen = repcap.InternalGen.Default) \n
		Enables or disables the tone list entries for multitone generation. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: tone_status: OFF | ON Comma-separated list of up to 20 values, tone 1 to tone 20 You can specify fewer than 20 values to configure only the beginning of the tone list."""
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:ENABle?')
		return Conversions.str_to_bool_list(response)
