from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDev:
	"""StandardDev commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("standardDev", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:DIGital:TTL:BERate:SDEViation \n
		Snippet: value: float = driver.afRf.measurement.digital.ttl.bitErrorRate.standardDev.fetch() \n
		Queries the bit error rate values of the measured signal via the TTL input path. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ber: Range: 0 % to 100 %, Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:DIGital:TTL:BERate:SDEViation?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:DIGital:TTL:BERate:SDEViation \n
		Snippet: value: float = driver.afRf.measurement.digital.ttl.bitErrorRate.standardDev.read() \n
		Queries the bit error rate values of the measured signal via the TTL input path. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ber: Range: 0 % to 100 %, Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:DIGital:TTL:BERate:SDEViation?', suppressed)
		return Conversions.str_to_float(response)
