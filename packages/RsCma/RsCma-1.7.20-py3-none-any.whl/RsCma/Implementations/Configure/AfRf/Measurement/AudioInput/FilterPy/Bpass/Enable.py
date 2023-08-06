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

	def set(self, enable: bool, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:BPASs:ENABle \n
		Snippet: driver.configure.afRf.measurement.audioInput.filterPy.bpass.enable.set(enable = False, audioInput = repcap.AudioInput.Default) \n
		Enables or disables the variable bandpass filter in an AF input path. \n
			:param enable: OFF | ON
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.bool_to_str(enable)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:BPASs:ENABle {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:BPASs:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.audioInput.filterPy.bpass.enable.get(audioInput = repcap.AudioInput.Default) \n
		Enables or disables the variable bandpass filter in an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: enable: OFF | ON"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:BPASs:ENABle?')
		return Conversions.str_to_bool(response)
