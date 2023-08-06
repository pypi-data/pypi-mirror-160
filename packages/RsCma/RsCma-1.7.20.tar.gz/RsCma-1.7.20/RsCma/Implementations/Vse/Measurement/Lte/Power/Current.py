from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def read(self) -> float:
		"""SCPI: READ:VSE:MEASurement<Instance>:LTE:POWer:CURRent \n
		Snippet: value: float = driver.vse.measurement.lte.power.current.read() \n
		Query LTE power results. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: Power value of the LTE signal Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:VSE:MEASurement<Instance>:LTE:POWer:CURRent?', suppressed)
		return Conversions.str_to_float(response)

	def fetch(self) -> float:
		"""SCPI: FETCh:VSE:MEASurement<Instance>:LTE:POWer:CURRent \n
		Snippet: value: float = driver.vse.measurement.lte.power.current.fetch() \n
		Query LTE power results. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: power: Power value of the LTE signal Unit: dBm"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:VSE:MEASurement<Instance>:LTE:POWer:CURRent?', suppressed)
		return Conversions.str_to_float(response)
