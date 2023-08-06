from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Coffset:
	"""Coffset commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("coffset", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:COFFset \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rifBandwidth.coffset.fetch() \n
		Query the center frequency offset. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: center_offset: Center frequency offset Range: -100 kHz to 100 kHz, Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:COFFset?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:COFFset \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rifBandwidth.coffset.read() \n
		Query the center frequency offset. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: center_offset: Center frequency offset Range: -100 kHz to 100 kHz, Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:COFFset?', suppressed)
		return Conversions.str_to_float(response)
