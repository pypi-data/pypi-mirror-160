from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fmoddepth:
	"""Fmoddepth commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fmoddepth", core, parent)

	def get(self, frequencyLobe=repcap.FrequencyLobe.Nr1) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:FMODdepth<nr> \n
		Snippet: value: float = driver.source.avionics.generator.ils.localizer.afSettings.fmoddepth.get(frequencyLobe = repcap.FrequencyLobe.Nr1) \n
		Queries the modulation depth for one lobe. \n
			:param frequencyLobe: optional repeated capability selector. Default value: Nr1
			:return: freq_1: Range: 0 % to 100 %, Unit: %"""
		frequencyLobe_cmd_val = self._cmd_group.get_repcap_cmd_value(frequencyLobe, repcap.FrequencyLobe)
		response = self._core.io.query_str(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:AFSettings:FMODdepth{frequencyLobe_cmd_val}?')
		return Conversions.str_to_float(response)
