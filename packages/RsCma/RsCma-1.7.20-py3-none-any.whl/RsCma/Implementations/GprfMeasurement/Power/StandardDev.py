from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StandardDev:
	"""StandardDev commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("standardDev", core, parent)

	def calculate(self) -> List[float or bool]:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:POWer:SDEViation \n
		Snippet: value: List[float or bool] = driver.gprfMeasurement.power.standardDev.calculate() \n
		Query the 'Standard Deviation' result. CALCulate commands return an error indicator instead of a power value. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power_std_dev_cur: (float or boolean items) 'Standard Deviation' result Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:GPRF:MEASurement<Instance>:POWer:SDEViation?', suppressed)
		return Conversions.str_to_float_or_bool_list(response)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:POWer:SDEViation \n
		Snippet: value: List[float] = driver.gprfMeasurement.power.standardDev.fetch() \n
		Query the 'Standard Deviation' result. CALCulate commands return an error indicator instead of a power value. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power_std_dev_cur: 'Standard Deviation' result Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:POWer:SDEViation?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:GPRF:MEASurement<Instance>:POWer:SDEViation \n
		Snippet: value: List[float] = driver.gprfMeasurement.power.standardDev.read() \n
		Query the 'Standard Deviation' result. CALCulate commands return an error indicator instead of a power value. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power_std_dev_cur: 'Standard Deviation' result Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:GPRF:MEASurement<Instance>:POWer:SDEViation?', suppressed)
		return response
