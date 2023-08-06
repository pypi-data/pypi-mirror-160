from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.ArgSingleSuppressed import ArgSingleSuppressed
from ........Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:DEMRight:AFSignal:DELTa:MAXimum \n
		Snippet: value: float = driver.afRf.measurement.multiEval.demodRight.afSignal.delta.maximum.fetch() \n
		Query the AF frequency results for the right demodulator channel. The commands are only relevant for FM stereo.
		The results are related to the right audio channel. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: frequency: Delta frequency value of the AF signal Range: 0 Hz to 21 kHz, Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:DEMRight:AFSignal:DELTa:MAXimum?', suppressed)
		return Conversions.str_to_float(response)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:DEMRight:AFSignal:DELTa:MAXimum \n
		Snippet: value: float = driver.afRf.measurement.multiEval.demodRight.afSignal.delta.maximum.read() \n
		Query the AF frequency results for the right demodulator channel. The commands are only relevant for FM stereo.
		The results are related to the right audio channel. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: frequency: Delta frequency value of the AF signal Range: 0 Hz to 21 kHz, Unit: Hz"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:DEMRight:AFSignal:DELTa:MAXimum?', suppressed)
		return Conversions.str_to_float(response)
