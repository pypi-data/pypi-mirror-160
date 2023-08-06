from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FreqError:
	"""FreqError commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("freqError", core, parent)

	def fetch(self) -> int:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:FREQuency:COUNter:FERRor \n
		Snippet: value: int = driver.afRf.measurement.frequency.counter.freqError.fetch() \n
		Queries the frequency error determined by the search procedure. The error is calculated as counted frequency minus
		configured analyzer frequency. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: frequency_error: Range: -3 GHz to 3 GHz, Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:FREQuency:COUNter:FERRor?', suppressed)
		return Conversions.str_to_int(response)
