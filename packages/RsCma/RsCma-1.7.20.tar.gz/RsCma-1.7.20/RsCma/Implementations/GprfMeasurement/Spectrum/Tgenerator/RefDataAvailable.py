from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RefDataAvailable:
	"""RefDataAvailable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("refDataAvailable", core, parent)

	def fetch(self) -> bool:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:SPECtrum:TGENerator:RDAVailable \n
		Snippet: value: bool = driver.gprfMeasurement.spectrum.tgenerator.refDataAvailable.fetch() \n
		Queries whether valid calibration results are available (ON) or not (OFF) . \n
			:return: ref_data_state: OFF | ON"""
		response = self._core.io.query_str(f'FETCh:GPRF:MEASurement<Instance>:SPECtrum:TGENerator:RDAVailable?')
		return Conversions.str_to_bool(response)
