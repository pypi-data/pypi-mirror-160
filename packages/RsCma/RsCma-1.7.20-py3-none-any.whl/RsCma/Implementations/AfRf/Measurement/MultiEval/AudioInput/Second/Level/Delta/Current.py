from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .........Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:AIN:SECond:LEVel:DELTa:CURRent \n
		Snippet: value: float = driver.afRf.measurement.multiEval.audioInput.second.level.delta.current.fetch() \n
		Query delta results for AF level at AF2. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: level: Unit: V"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:AIN:SECond:LEVel:DELTa:CURRent?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:AIN:SECond:LEVel:DELTa:CURRent \n
		Snippet: value: float = driver.afRf.measurement.multiEval.audioInput.second.level.delta.current.read() \n
		Query delta results for AF level at AF2. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: level: Unit: V"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:AIN:SECond:LEVel:DELTa:CURRent?', suppressed)
		return Conversions.str_to_float(response)
