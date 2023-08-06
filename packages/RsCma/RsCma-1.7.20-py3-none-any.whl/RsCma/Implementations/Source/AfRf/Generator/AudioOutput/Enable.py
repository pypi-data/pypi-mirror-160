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

	def set(self, enable: bool, audioOutput=repcap.AudioOutput.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AOUT<nr>:ENABle \n
		Snippet: driver.source.afRf.generator.audioOutput.enable.set(enable = False, audioOutput = repcap.AudioOutput.Default) \n
		Enables or disables an AF OUT connector. \n
			:param enable: OFF | ON
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
		"""
		param = Conversions.bool_to_str(enable)
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:AOUT{audioOutput_cmd_val}:ENABle {param}')

	def get(self, audioOutput=repcap.AudioOutput.Default) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AOUT<nr>:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.audioOutput.enable.get(audioOutput = repcap.AudioOutput.Default) \n
		Enables or disables an AF OUT connector. \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:return: enable: OFF | ON"""
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:AOUT{audioOutput_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
