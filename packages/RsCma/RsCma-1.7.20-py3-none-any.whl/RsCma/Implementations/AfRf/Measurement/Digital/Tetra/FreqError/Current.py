from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:DIGital:TETRa:FERRor:CURRent \n
		Snippet: value: float = driver.afRf.measurement.digital.tetra.freqError.current.fetch() \n
		Query the current frequency error for TETRA. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: freq_error: Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:DIGital:TETRa:FERRor:CURRent?', suppressed)
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def calculate(self) -> enums.ResultStatus:
		"""SCPI: CALCulate:AFRF:MEASurement<Instance>:DIGital:TETRa:FERRor:CURRent \n
		Snippet: value: enums.ResultStatus = driver.afRf.measurement.digital.tetra.freqError.current.calculate() \n
		Query the current frequency error for TETRA. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: freq_error: Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:AFRF:MEASurement<Instance>:DIGital:TETRa:FERRor:CURRent?', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.ResultStatus)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:DIGital:TETRa:FERRor:CURRent \n
		Snippet: value: float = driver.afRf.measurement.digital.tetra.freqError.current.read() \n
		Query the current frequency error for TETRA. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: freq_error: Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:DIGital:TETRa:FERRor:CURRent?', suppressed)
		return Conversions.str_to_float(response)
