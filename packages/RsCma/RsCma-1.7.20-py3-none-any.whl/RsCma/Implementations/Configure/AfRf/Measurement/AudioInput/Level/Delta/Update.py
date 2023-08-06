from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Update:
	"""Update commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("update", core, parent)

	def set(self, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:LEVel:DELTa:UPDate \n
		Snippet: driver.configure.afRf.measurement.audioInput.level.delta.update.set(audioInput = repcap.AudioInput.Default) \n
		Triggers the update of the AF level measurement reference value. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:LEVel:DELTa:UPDate')

	def set_with_opc(self, audioInput=repcap.AudioInput.Default, opc_timeout_ms: int = -1) -> None:
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:LEVel:DELTa:UPDate \n
		Snippet: driver.configure.afRf.measurement.audioInput.level.delta.update.set_with_opc(audioInput = repcap.AudioInput.Default) \n
		Triggers the update of the AF level measurement reference value. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:LEVel:DELTa:UPDate', opc_timeout_ms)
