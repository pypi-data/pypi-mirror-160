from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Repetitions:
	"""Repetitions commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("repetitions", core, parent)

	def fetch(self, audioInput=repcap.AudioInput.Default) -> int:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN<Nr>:REPetitions \n
		Snippet: value: int = driver.afRf.measurement.multiEval.tones.audioInput.repetitions.fetch(audioInput = repcap.AudioInput.Default) \n
		Query the number of measured tone sequences. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: repetitions: No help available"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN{audioInput_cmd_val}:REPetitions?', suppressed)
		return Conversions.str_to_int(response)

	def read(self, audioInput=repcap.AudioInput.Default) -> int:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN<Nr>:REPetitions \n
		Snippet: value: int = driver.afRf.measurement.multiEval.tones.audioInput.repetitions.read(audioInput = repcap.AudioInput.Default) \n
		Query the number of measured tone sequences. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: repetitions: No help available"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN{audioInput_cmd_val}:REPetitions?', suppressed)
		return Conversions.str_to_int(response)
