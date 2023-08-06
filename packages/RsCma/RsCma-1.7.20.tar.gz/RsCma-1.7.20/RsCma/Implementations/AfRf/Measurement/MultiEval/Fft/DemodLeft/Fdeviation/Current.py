from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:FFT:DEMLeft:FDEViation:CURRent \n
		Snippet: value: List[float] = driver.afRf.measurement.multiEval.fft.demodLeft.fdeviation.current.fetch() \n
		Query the contents of the spectrum diagram for the left demodulator channel and FM demodulation or FM stereo demodulation.
		For FM stereo, these results are related to the left audio channel. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: Comma-separated list of 1793 frequency deviation or audio deviation values (diagram from left to right) Unit: dBHz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:FFT:DEMLeft:FDEViation:CURRent?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:FFT:DEMLeft:FDEViation:CURRent \n
		Snippet: value: List[float] = driver.afRf.measurement.multiEval.fft.demodLeft.fdeviation.current.read() \n
		Query the contents of the spectrum diagram for the left demodulator channel and FM demodulation or FM stereo demodulation.
		For FM stereo, these results are related to the left audio channel. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: Comma-separated list of 1793 frequency deviation or audio deviation values (diagram from left to right) Unit: dBHz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:FFT:DEMLeft:FDEViation:CURRent?', suppressed)
		return response
