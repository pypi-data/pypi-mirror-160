from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self, audioInput=repcap.AudioInput.Default) -> List[float]:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:AIN<Nr>:PVTime:CURRent \n
		Snippet: value: List[float] = driver.afRf.measurement.multiEval.oscilloscope.audioInput.powerVsTime.current.fetch(audioInput = repcap.AudioInput.Default) \n
		Query the contents of the AF oscilloscope diagram for an AF input path. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: power_vs_time: Comma-separated list of 960 audio level values (diagram from left to right) Unit: V"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:AIN{audioInput_cmd_val}:PVTime:CURRent?', suppressed)
		return response

	def read(self, audioInput=repcap.AudioInput.Default) -> List[float]:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:AIN<Nr>:PVTime:CURRent \n
		Snippet: value: List[float] = driver.afRf.measurement.multiEval.oscilloscope.audioInput.powerVsTime.current.read(audioInput = repcap.AudioInput.Default) \n
		Query the contents of the AF oscilloscope diagram for an AF input path. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: power_vs_time: Comma-separated list of 960 audio level values (diagram from left to right) Unit: V"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:AIN{audioInput_cmd_val}:PVTime:CURRent?', suppressed)
		return response
