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
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:NLEVel:TRACe \n
		Snippet: value: List[float] = driver.afRf.measurement.searchRoutines.rifBandwidth.nlevel.trace.fetch() \n
		Query the noise level values for the RX IF bandwidth measurement. These values are the y-values for the points in the RX
		IF bandwidth diagram. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: noise_level: Comma-separated list of noise level values Unit: V"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:NLEVel:TRACe?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:NLEVel:TRACe \n
		Snippet: value: List[float] = driver.afRf.measurement.searchRoutines.rifBandwidth.nlevel.trace.read() \n
		Query the noise level values for the RX IF bandwidth measurement. These values are the y-values for the points in the RX
		IF bandwidth diagram. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: noise_level: Comma-separated list of noise level values Unit: V"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:NLEVel:TRACe?', suppressed)
		return response
