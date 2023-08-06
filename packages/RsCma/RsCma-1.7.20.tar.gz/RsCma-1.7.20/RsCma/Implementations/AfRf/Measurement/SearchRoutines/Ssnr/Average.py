from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:SSNR:AVERage \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.ssnr.average.fetch() \n
		Query the SNR results for the 'Switched SNR' search routine. A statistical evaluation of the SNR values is returned. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ssnr: Switched SNR value Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:SSNR:AVERage?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:SSNR:AVERage \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.ssnr.average.read() \n
		Query the SNR results for the 'Switched SNR' search routine. A statistical evaluation of the SNR values is returned. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: ssnr: Switched SNR value Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:SROutines:SSNR:AVERage?', suppressed)
		return Conversions.str_to_float(response)
