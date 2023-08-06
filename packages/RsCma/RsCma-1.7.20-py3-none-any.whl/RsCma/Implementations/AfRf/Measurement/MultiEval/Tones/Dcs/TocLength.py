from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TocLength:
	"""TocLength commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tocLength", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOCLength \n
		Snippet: value: float = driver.afRf.measurement.multiEval.tones.dcs.tocLength.fetch() \n
		Query the duration of the last received turn-off code. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: off_code_length: Unit: s"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOCLength?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOCLength \n
		Snippet: value: float = driver.afRf.measurement.multiEval.tones.dcs.tocLength.read() \n
		Query the duration of the last received turn-off code. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: off_code_length: Unit: s"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:TOCLength?', suppressed)
		return Conversions.str_to_float(response)
