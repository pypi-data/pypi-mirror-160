from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmatches:
	"""Dmatches commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmatches", core, parent)

	def fetch(self) -> int:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:DMATches \n
		Snippet: value: int = driver.afRf.measurement.multiEval.tones.dcs.dmatches.fetch() \n
		Query the number of received code words that matched the expected code word. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: detected_matches: Number of matches"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:DMATches?', suppressed)
		return Conversions.str_to_int(response)

	def read(self) -> int:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:DMATches \n
		Snippet: value: int = driver.afRf.measurement.multiEval.tones.dcs.dmatches.read() \n
		Query the number of received code words that matched the expected code word. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: detected_matches: Number of matches"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:DMATches?', suppressed)
		return Conversions.str_to_int(response)
