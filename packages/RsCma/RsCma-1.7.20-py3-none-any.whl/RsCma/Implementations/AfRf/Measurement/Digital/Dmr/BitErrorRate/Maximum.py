from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:DIGital:DMR:BERate:MAXimum \n
		Snippet: value: float = driver.afRf.measurement.digital.dmr.bitErrorRate.maximum.fetch() \n
		Query the maximum bit error rate values measured for a DMR signal. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ber: Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:DIGital:DMR:BERate:MAXimum?', suppressed)
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def calculate(self) -> enums.ResultStatus:
		"""SCPI: CALCulate:AFRF:MEASurement<Instance>:DIGital:DMR:BERate:MAXimum \n
		Snippet: value: enums.ResultStatus = driver.afRf.measurement.digital.dmr.bitErrorRate.maximum.calculate() \n
		Query the maximum bit error rate values measured for a DMR signal. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ber: Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:AFRF:MEASurement<Instance>:DIGital:DMR:BERate:MAXimum?', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.ResultStatus)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:DIGital:DMR:BERate:MAXimum \n
		Snippet: value: float = driver.afRf.measurement.digital.dmr.bitErrorRate.maximum.read() \n
		Query the maximum bit error rate values measured for a DMR signal. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ber: Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:DIGital:DMR:BERate:MAXimum?', suppressed)
		return Conversions.str_to_float(response)
