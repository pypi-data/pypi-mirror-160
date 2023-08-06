from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sensitivity:
	"""Sensitivity commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sensitivity", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RSENsitivity:SENSitivity \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rsensitivity.sensitivity.fetch() \n
		Query the sensitivity level of the RX sensitivity search routine. CALCulate commands return error indicators instead of
		measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: rx_sensitivity_level: Measured RX sensitivity level (RF level) Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RSENsitivity:SENSitivity?', suppressed)
		return Conversions.str_to_float(response)

	def calculate(self) -> float:
		"""SCPI: CALCulate:AFRF:MEASurement<Instance>:SROutines:RSENsitivity:SENSitivity \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rsensitivity.sensitivity.calculate() \n
		Query the sensitivity level of the RX sensitivity search routine. CALCulate commands return error indicators instead of
		measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: rx_sensitivity_level: Measured RX sensitivity level (RF level) Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:AFRF:MEASurement<Instance>:SROutines:RSENsitivity:SENSitivity?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:RSENsitivity:SENSitivity \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.rsensitivity.sensitivity.read() \n
		Query the sensitivity level of the RX sensitivity search routine. CALCulate commands return error indicators instead of
		measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: rx_sensitivity_level: Measured RX sensitivity level (RF level) Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:SROutines:RSENsitivity:SENSitivity?', suppressed)
		return Conversions.str_to_float(response)
