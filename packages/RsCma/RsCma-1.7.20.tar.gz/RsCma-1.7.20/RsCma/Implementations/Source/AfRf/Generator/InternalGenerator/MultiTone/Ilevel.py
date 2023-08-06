from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ilevel:
	"""Ilevel commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ilevel", core, parent)

	def set(self, ilevel: List[float], internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:ILEVel \n
		Snippet: driver.source.afRf.generator.internalGenerator.multiTone.ilevel.set(ilevel = [1.1, 2.2, 3.3], internalGen = repcap.InternalGen.Default) \n
		Configures the levels of all tones of a multitone signal for edit mode INDividual. In edit mode TOTal, you can only query
		the levels, but not configure them. \n
			:param ilevel: Comma-separated list of up to 20 levels, for tone 1 to tone 20 You can specify fewer than 20 values to configure only the beginning of the tone list.
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
		"""
		param = Conversions.list_to_csv_str(ilevel)
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:ILEVel {param}')

	def get(self, internalGen=repcap.InternalGen.Default) -> List[float]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:ILEVel \n
		Snippet: value: List[float] = driver.source.afRf.generator.internalGenerator.multiTone.ilevel.get(internalGen = repcap.InternalGen.Default) \n
		Configures the levels of all tones of a multitone signal for edit mode INDividual. In edit mode TOTal, you can only query
		the levels, but not configure them. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: ilevel: Comma-separated list of up to 20 levels, for tone 1 to tone 20 You can specify fewer than 20 values to configure only the beginning of the tone list."""
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		response = self._core.io.query_bin_or_ascii_float_list(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:ILEVel?')
		return response
