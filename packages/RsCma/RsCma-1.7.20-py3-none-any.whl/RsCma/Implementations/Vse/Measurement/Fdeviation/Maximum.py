from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:VSE:MEASurement<Instance>:FDEViation:MAXimum \n
		Snippet: value: float = driver.vse.measurement.fdeviation.maximum.fetch() \n
		Query the FSK deviation results (part of the demodulation results) . \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: fsk_deviation: Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:VSE:MEASurement<Instance>:FDEViation:MAXimum?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:VSE:MEASurement<Instance>:FDEViation:MAXimum \n
		Snippet: value: float = driver.vse.measurement.fdeviation.maximum.read() \n
		Query the FSK deviation results (part of the demodulation results) . \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: fsk_deviation: Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:VSE:MEASurement<Instance>:FDEViation:MAXimum?', suppressed)
		return Conversions.str_to_float(response)
