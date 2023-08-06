from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Xvalues:
	"""Xvalues commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("xvalues", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:XVALues \n
		Snippet: value: List[float] = driver.gprfMeasurement.spectrum.zeroSpan.xvalues.fetch() \n
		Queries the x-values of the result traces in 'Zero Span' mode. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: xvalues: Comma-separated list of 1001 time values Unit: s"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:XVALues?', suppressed)
		return response
