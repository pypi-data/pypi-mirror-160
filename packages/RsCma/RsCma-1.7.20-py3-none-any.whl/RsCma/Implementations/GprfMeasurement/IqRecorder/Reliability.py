from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reliability:
	"""Reliability commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reliability", core, parent)

	def fetch(self) -> int:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:IQRecorder:RELiability \n
		Snippet: value: int = driver.gprfMeasurement.iqRecorder.reliability.fetch() \n
		Queries the reliability indicator for the I/Q recorder measurement, see 'Reliability indicator values'. \n
			:return: reliability_flag: Two equal values, separated by a comma (for example 0,0 for 'OK')"""
		response = self._core.io.query_str(f'FETCh:GPRF:MEASurement<Instance>:IQRecorder:RELiability?')
		return Conversions.str_to_int(response)
