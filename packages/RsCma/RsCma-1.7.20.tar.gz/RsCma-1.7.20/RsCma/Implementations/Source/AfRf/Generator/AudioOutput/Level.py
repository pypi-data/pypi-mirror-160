from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Level:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def set(self, level: float, audioOutput=repcap.AudioOutput.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AOUT<nr>:LEVel \n
		Snippet: driver.source.afRf.generator.audioOutput.level.set(level = 1.0, audioOutput = repcap.AudioOutput.Default) \n
		No command help available \n
			:param level: No help available
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
		"""
		param = Conversions.decimal_value_to_str(level)
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:AOUT{audioOutput_cmd_val}:LEVel {param}')

	def get(self, audioOutput=repcap.AudioOutput.Default) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AOUT<nr>:LEVel \n
		Snippet: value: float = driver.source.afRf.generator.audioOutput.level.get(audioOutput = repcap.AudioOutput.Default) \n
		No command help available \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:return: level: No help available"""
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:AOUT{audioOutput_cmd_val}:LEVel?')
		return Conversions.str_to_float(response)
