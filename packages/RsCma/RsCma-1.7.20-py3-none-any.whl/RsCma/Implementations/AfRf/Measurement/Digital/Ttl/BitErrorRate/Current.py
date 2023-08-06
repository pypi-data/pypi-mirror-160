from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:DIGital:TTL:BERate:CURRent \n
		Snippet: value: float = driver.afRf.measurement.digital.ttl.bitErrorRate.current.fetch() \n
		Query the current digital measurement results of BER for the TTL path. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ber: Range: 0 % to 100 %, Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:DIGital:TTL:BERate:CURRent?', suppressed)
		return Conversions.str_to_float(response)

	def calculate(self) -> float or bool:
		"""SCPI: CALCulate:AFRF:MEASurement<Instance>:DIGital:TTL:BERate:CURRent \n
		Snippet: value: float or bool = driver.afRf.measurement.digital.ttl.bitErrorRate.current.calculate() \n
		Query the current digital measurement results of BER for the TTL path. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ber: (float or boolean) Range: 0 % to 100 %, Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:AFRF:MEASurement<Instance>:DIGital:TTL:BERate:CURRent?', suppressed)
		return Conversions.str_to_float_or_bool(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:DIGital:TTL:BERate:CURRent \n
		Snippet: value: float = driver.afRf.measurement.digital.ttl.bitErrorRate.current.read() \n
		Query the current digital measurement results of BER for the TTL path. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ber: Range: 0 % to 100 %, Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:DIGital:TTL:BERate:CURRent?', suppressed)
		return Conversions.str_to_float(response)
