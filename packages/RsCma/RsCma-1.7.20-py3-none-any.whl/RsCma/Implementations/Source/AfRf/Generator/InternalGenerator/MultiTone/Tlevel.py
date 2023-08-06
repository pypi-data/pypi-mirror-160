from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tlevel:
	"""Tlevel commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tlevel", core, parent)

	def set(self, tlevel: List[float], internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:TLEVel \n
		Snippet: driver.source.afRf.generator.internalGenerator.multiTone.tlevel.set(tlevel = [1.1, 2.2, 3.3], internalGen = repcap.InternalGen.Default) \n
		Sets the total level of a multitone signal for edit mode TOTal. In edit mode INDividual, you can only query the total
		level, but not configure it. \n
			:param tlevel: Total level
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
		"""
		param = Conversions.list_to_csv_str(tlevel)
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:TLEVel {param}')

	def get(self, internalGen=repcap.InternalGen.Default) -> List[float]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:TLEVel \n
		Snippet: value: List[float] = driver.source.afRf.generator.internalGenerator.multiTone.tlevel.get(internalGen = repcap.InternalGen.Default) \n
		Sets the total level of a multitone signal for edit mode TOTal. In edit mode INDividual, you can only query the total
		level, but not configure it. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: tlevel: Total level"""
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		response = self._core.io.query_bin_or_ascii_float_list(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:TLEVel?')
		return response
