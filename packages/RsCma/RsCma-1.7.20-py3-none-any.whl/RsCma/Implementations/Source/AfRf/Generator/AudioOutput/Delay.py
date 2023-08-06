from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	def set(self, enable: bool, audioOutput=repcap.AudioOutput.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AOUT<nr>:DELay \n
		Snippet: driver.source.afRf.generator.audioOutput.delay.set(enable = False, audioOutput = repcap.AudioOutput.Default) \n
		No command help available \n
			:param enable: No help available
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
		"""
		param = Conversions.bool_to_str(enable)
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:AOUT{audioOutput_cmd_val}:DELay {param}')

	def get(self, audioOutput=repcap.AudioOutput.Default) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AOUT<nr>:DELay \n
		Snippet: value: bool = driver.source.afRf.generator.audioOutput.delay.get(audioOutput = repcap.AudioOutput.Default) \n
		No command help available \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:return: enable: No help available"""
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:AOUT{audioOutput_cmd_val}:DELay?')
		return Conversions.str_to_bool(response)
