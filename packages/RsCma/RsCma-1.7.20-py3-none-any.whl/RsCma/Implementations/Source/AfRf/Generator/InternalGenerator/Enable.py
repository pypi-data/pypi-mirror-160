from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def get(self, internalGen=repcap.InternalGen.Default) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.internalGenerator.enable.get(internalGen = repcap.InternalGen.Default) \n
		Queries whether an internal audio generator is assigned to an audio output path. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: enable: OFF | ON OFF Generator disabled / not assigned to an output path ON Generator enabled / assigned to an output path"""
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
