from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:VOIP:DELay:CURRent \n
		Snippet: value: float = driver.afRf.measurement.voip.delay.current.fetch() \n
		Queries the current scalar results for VoIP audio delay. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: delay: Unit: s"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:VOIP:DELay:CURRent?', suppressed)
		return Conversions.str_to_float(response)
