from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self, audioInput=repcap.AudioInput.Default) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:AIN<Nr>:DELay:CURRent \n
		Snippet: value: float = driver.afRf.measurement.audioInput.delay.current.fetch(audioInput = repcap.AudioInput.Default) \n
		Queries the current scalar results for AF1 and AF2 audio delay. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: delay: Unit: s"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:DELay:CURRent?', suppressed)
		return Conversions.str_to_float(response)
