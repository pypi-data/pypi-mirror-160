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
		"""SCPI: FETCh:VSE:MEASurement<Instance>:EDIagram:CURRent \n
		Snippet: value: List[float] = driver.vse.measurement.ediagram.current.fetch() \n
		Query the eye diagram current results. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: eye_diagram: Comma-separated list of 1020 frequency deviation values. The list has 60 lines with 17 values each. Each line in the diagram is interpolated from 17 values. Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:VSE:MEASurement<Instance>:EDIagram:CURRent?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:VSE:MEASurement<Instance>:EDIagram:CURRent \n
		Snippet: value: List[float] = driver.vse.measurement.ediagram.current.read() \n
		Query the eye diagram current results. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: eye_diagram: Comma-separated list of 1020 frequency deviation values. The list has 60 lines with 17 values each. Each line in the diagram is interpolated from 17 values. Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:VSE:MEASurement<Instance>:EDIagram:CURRent?', suppressed)
		return response
