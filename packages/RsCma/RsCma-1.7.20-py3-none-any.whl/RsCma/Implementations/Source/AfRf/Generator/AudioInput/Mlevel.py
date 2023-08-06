from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mlevel:
	"""Mlevel commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mlevel", core, parent)

	def set(self, level: float, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AIN<nr>:MLEVel \n
		Snippet: driver.source.afRf.generator.audioInput.mlevel.set(level = 1.0, audioInput = repcap.AudioInput.Default) \n
		No command help available \n
			:param level: No help available
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.decimal_value_to_str(level)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:AIN{audioInput_cmd_val}:MLEVel {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AIN<nr>:MLEVel \n
		Snippet: value: float = driver.source.afRf.generator.audioInput.mlevel.get(audioInput = repcap.AudioInput.Default) \n
		No command help available \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: level: No help available"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:AIN{audioInput_cmd_val}:MLEVel?')
		return Conversions.str_to_float(response)
