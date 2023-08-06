from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OfsQuality:
	"""OfsQuality commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ofsQuality", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFSQuality \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rsquelch.ofsQuality.fetch() \n
		Query the signal quality at the squelch switch-off level. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: off_sig_quality: Signal quality value at squelch switch-off level Range: -150 dB to 150 dB, Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFSQuality?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFSQuality \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rsquelch.ofsQuality.read() \n
		Query the signal quality at the squelch switch-off level. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: off_sig_quality: Signal quality value at squelch switch-off level Range: -150 dB to 150 dB, Unit: dB"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:SROutines:RSQuelch:OFSQuality?', suppressed)
		return Conversions.str_to_float(response)
