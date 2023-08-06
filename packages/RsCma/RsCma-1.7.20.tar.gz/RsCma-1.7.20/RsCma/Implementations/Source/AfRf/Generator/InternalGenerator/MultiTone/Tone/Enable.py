from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, tone_status: bool, internalGen=repcap.InternalGen.Default, toneNumber=repcap.ToneNumber.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:TONE<no>:ENABle \n
		Snippet: driver.source.afRf.generator.internalGenerator.multiTone.tone.enable.set(tone_status = False, internalGen = repcap.InternalGen.Default, toneNumber = repcap.ToneNumber.Default) \n
		Enables or disables a selected tone list entry for multitone generation. \n
			:param tone_status: OFF | ON
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:param toneNumber: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tone')
		"""
		param = Conversions.bool_to_str(tone_status)
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		toneNumber_cmd_val = self._cmd_group.get_repcap_cmd_value(toneNumber, repcap.ToneNumber)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:TONE{toneNumber_cmd_val}:ENABle {param}')

	def get(self, internalGen=repcap.InternalGen.Default, toneNumber=repcap.ToneNumber.Default) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:TONE<no>:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.internalGenerator.multiTone.tone.enable.get(internalGen = repcap.InternalGen.Default, toneNumber = repcap.ToneNumber.Default) \n
		Enables or disables a selected tone list entry for multitone generation. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:param toneNumber: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Tone')
			:return: tone_status: OFF | ON"""
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		toneNumber_cmd_val = self._cmd_group.get_repcap_cmd_value(toneNumber, repcap.ToneNumber)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:TONE{toneNumber_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
