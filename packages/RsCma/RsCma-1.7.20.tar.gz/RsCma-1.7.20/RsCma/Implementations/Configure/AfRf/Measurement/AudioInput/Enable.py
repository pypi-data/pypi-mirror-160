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

	def set(self, test_af: bool, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:ENABle \n
		Snippet: driver.configure.afRf.measurement.audioInput.enable.set(test_af = False, audioInput = repcap.AudioInput.Default) \n
		Enables or disables an AF IN connector. \n
			:param test_af: OFF | ON Switches the connector off or on
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.bool_to_str(test_af)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:ENABle {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.audioInput.enable.get(audioInput = repcap.AudioInput.Default) \n
		Enables or disables an AF IN connector. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: test_af: OFF | ON Switches the connector off or on"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
