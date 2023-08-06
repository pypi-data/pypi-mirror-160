from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AgcPeriod:
	"""AgcPeriod commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("agcPeriod", core, parent)

	def set(self, agc_period: int, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:AGCPeriod \n
		Snippet: driver.configure.afRf.measurement.audioInput.agcPeriod.set(agc_period = 1, audioInput = repcap.AudioInput.Default) \n
		No command help available \n
			:param agc_period: No help available
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.decimal_value_to_str(agc_period)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:AGCPeriod {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:AGCPeriod \n
		Snippet: value: int = driver.configure.afRf.measurement.audioInput.agcPeriod.get(audioInput = repcap.AudioInput.Default) \n
		No command help available \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: agc_period: No help available"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:AGCPeriod?')
		return Conversions.str_to_int(response)
