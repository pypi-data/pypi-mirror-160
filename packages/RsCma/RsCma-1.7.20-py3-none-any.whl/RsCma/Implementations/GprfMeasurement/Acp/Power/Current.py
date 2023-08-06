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
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:ACP:POWer:CURRent \n
		Snippet: value: List[float] = driver.gprfMeasurement.acp.power.current.fetch() \n
		Query the absolute power results. There are separate commands for the current, average and maximum values. CALCulate
		commands return error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: Comma-separated list of five power values, one per channel: Channel -2, -1, 0, +1, +2 Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:ACP:POWer:CURRent?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:ACP:POWer:CURRent \n
		Snippet: value: List[float] = driver.gprfMeasurement.acp.power.current.read() \n
		Query the absolute power results. There are separate commands for the current, average and maximum values. CALCulate
		commands return error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: Comma-separated list of five power values, one per channel: Channel -2, -1, 0, +1, +2 Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:ACP:POWer:CURRent?', suppressed)
		return response

	def calculate(self) -> List[float or bool]:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:ACP:POWer:CURRent \n
		Snippet: value: List[float or bool] = driver.gprfMeasurement.acp.power.current.calculate() \n
		Query the absolute power results. There are separate commands for the current, average and maximum values. CALCulate
		commands return error indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: (float or boolean items) Comma-separated list of five power values, one per channel: Channel -2, -1, 0, +1, +2 Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:GPRF:MEASurement<Instance>:ACP:POWer:CURRent?', suppressed)
		return Conversions.str_to_float_or_bool_list(response)
