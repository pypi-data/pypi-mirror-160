from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("symbolRate", core, parent)

	def fetch(self) -> float:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:IQRecorder:SRATe \n
		Snippet: value: float = driver.gprfMeasurement.iqRecorder.symbolRate.fetch() \n
		Returns the maximum sample rate, resulting from the filter settings. \n
			:return: sample_rate: Unit: Hz"""
		response = self._core.io.query_str(f'FETCh:GPRF:MEASurement<Instance>:IQRecorder:SRATe?')
		return Conversions.str_to_float(response)
