from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:VSE:MEASurement<Instance>:SPECtrum:CURRent \n
		Snippet: value: List[float] = driver.vse.measurement.spectrum.current.fetch() \n
		Query the current power results of the measured spectrum. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:VSE:MEASurement<Instance>:SPECtrum:CURRent?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:VSE:MEASurement<Instance>:SPECtrum:CURRent \n
		Snippet: value: List[float] = driver.vse.measurement.spectrum.current.read() \n
		Query the current power results of the measured spectrum. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:VSE:MEASurement<Instance>:SPECtrum:CURRent?', suppressed)
		return response
