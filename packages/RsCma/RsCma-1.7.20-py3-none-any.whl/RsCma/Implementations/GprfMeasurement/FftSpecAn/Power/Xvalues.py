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
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:POWer:XVALues \n
		Snippet: value: List[float] = driver.gprfMeasurement.fftSpecAn.power.xvalues.fetch() \n
		Queries the x-values of the spectrum diagram. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: xvalues: Comma-separated list of 801 frequency values The frequency values cover the entire measured frequency span, from the lower end to the upper end. The frequency distance between two x-values equals span/800. Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:GPRF:MEASurement<Instance>:FFTSanalyzer:POWer:XVALues?', suppressed)
		return response
