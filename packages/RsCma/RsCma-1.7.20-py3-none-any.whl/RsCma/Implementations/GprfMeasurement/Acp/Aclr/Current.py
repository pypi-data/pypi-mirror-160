from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:ACP:ACLR:CURRent \n
		Snippet: value: List[float] = driver.gprfMeasurement.acp.aclr.current.fetch() \n
		Query the ACLR results. There are separate commands for the current, average, maximum and standard deviation values.
		CALCulate commands return error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: aclr: Comma-separated list of five ACLR values, one per channel: Channel -2, -1, 0, +1, +2 Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:ACP:ACLR:CURRent?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:ACP:ACLR:CURRent \n
		Snippet: value: List[float] = driver.gprfMeasurement.acp.aclr.current.read() \n
		Query the ACLR results. There are separate commands for the current, average, maximum and standard deviation values.
		CALCulate commands return error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: aclr: Comma-separated list of five ACLR values, one per channel: Channel -2, -1, 0, +1, +2 Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:ACP:ACLR:CURRent?', suppressed)
		return response

	def calculate(self) -> List[float or bool]:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:ACP:ACLR:CURRent \n
		Snippet: value: List[float or bool] = driver.gprfMeasurement.acp.aclr.current.calculate() \n
		Query the ACLR results. There are separate commands for the current, average, maximum and standard deviation values.
		CALCulate commands return error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: aclr: (float or boolean items) Comma-separated list of five ACLR values, one per channel: Channel -2, -1, 0, +1, +2 Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:GPRF:MEASurement<Instance>:ACP:ACLR:CURRent?', suppressed)
		return Conversions.str_to_float_or_bool_list(response)
