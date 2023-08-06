from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trace:
	"""Trace commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trace", core, parent)

	def fetch(self) -> List[float]:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:VOIP:LEVel:TRACe \n
		Snippet: value: List[float] = driver.afRf.measurement.searchRoutines.tsensitivity.voip.level.trace.fetch() \n
		Query the x-values of the points in the TX modulation sensitivity result diagram. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: af_level_list: Comma-separated list of AF levels of the VoIP path Unit: dBm0"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:VOIP:LEVel:TRACe?', suppressed)
		return response

	def read(self) -> List[float]:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:VOIP:LEVel:TRACe \n
		Snippet: value: List[float] = driver.afRf.measurement.searchRoutines.tsensitivity.voip.level.trace.read() \n
		Query the x-values of the points in the TX modulation sensitivity result diagram. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: af_level_list: Comma-separated list of AF levels of the VoIP path Unit: dBm0"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_bin_or_ascii_float_list_suppressed(f'READ:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:VOIP:LEVel:TRACe?', suppressed)
		return response
