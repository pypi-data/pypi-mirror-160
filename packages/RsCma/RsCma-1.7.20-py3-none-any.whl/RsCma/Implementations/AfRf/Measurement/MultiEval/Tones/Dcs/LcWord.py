from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LcWord:
	"""LcWord commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lcWord", core, parent)

	def fetch(self) -> str:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:LCWord \n
		Snippet: value: str = driver.afRf.measurement.multiEval.tones.dcs.lcWord.fetch() \n
		Query the code number of the last detected code word that matched the expected code word. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: last_code_word: Detected DCS code number as octal number"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:LCWord?', suppressed)
		return trim_str_response(response)

	def read(self) -> str:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:LCWord \n
		Snippet: value: str = driver.afRf.measurement.multiEval.tones.dcs.lcWord.read() \n
		Query the code number of the last detected code word that matched the expected code word. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: last_code_word: Detected DCS code number as octal number"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:LCWord?', suppressed)
		return trim_str_response(response)
