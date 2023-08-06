from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trace:
	"""Trace commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trace", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:SQUality:TRACe \n
		Snippet: value: List[float] = driver.afRf.measurement.searchRoutines.rsquelch.signalQuality.trace.fetch() \n
		Query the list of signal quality values for the squelch measurement. These values are the y-values for the points in the
		RX squelch diagram. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: sig_qual_list: Comma-separated list of signal quality values Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:SQUality:TRACe?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:RSQuelch:SQUality:TRACe \n
		Snippet: value: List[float] = driver.afRf.measurement.searchRoutines.rsquelch.signalQuality.trace.read() \n
		Query the list of signal quality values for the squelch measurement. These values are the y-values for the points in the
		RX squelch diagram. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: sig_qual_list: Comma-separated list of signal quality values Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:AFRF:MEASurement<Instance>:SROutines:RSQuelch:SQUality:TRACe?', suppressed)
		return response
