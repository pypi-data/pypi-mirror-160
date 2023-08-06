from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Condition:
	"""Condition commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("condition", core, parent)

	def get(self, bit=repcap.Bit.Default) -> bool:
		"""SCPI: STATus:QUEStionable:BIT<bitno>:CONDition \n
		Snippet: value: bool = driver.status.questionable.bit.condition.get(bit = repcap.Bit.Default) \n
		No command help available \n
			:param bit: optional repeated capability selector. Default value: Nr8 (settable in the interface 'Bit')
			:return: register_bit: No help available"""
		bit_cmd_val = self._cmd_group.get_repcap_cmd_value(bit, repcap.Bit)
		response = self._core.io.query_str(f'STATus:QUEStionable:BIT{bit_cmd_val}:CONDition?')
		return Conversions.str_to_bool(response)
