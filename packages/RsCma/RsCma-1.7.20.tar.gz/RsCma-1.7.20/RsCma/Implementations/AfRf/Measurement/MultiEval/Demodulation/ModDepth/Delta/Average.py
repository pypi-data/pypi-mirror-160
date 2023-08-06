from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:DEModulation:MDEPth:DELTa:AVERage \n
		Snippet: value: float = driver.afRf.measurement.multiEval.demodulation.modDepth.delta.average.fetch() \n
		Query the demodulation delta results for AM demodulation. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: mod_depth: Range: 0.01 dB to 100.00 dB , Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:DEModulation:MDEPth:DELTa:AVERage?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:DEModulation:MDEPth:DELTa:AVERage \n
		Snippet: value: float = driver.afRf.measurement.multiEval.demodulation.modDepth.delta.average.read() \n
		Query the demodulation delta results for AM demodulation. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: mod_depth: Range: 0.01 dB to 100.00 dB , Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:DEModulation:MDEPth:DELTa:AVERage?', suppressed)
		return Conversions.str_to_float(response)
