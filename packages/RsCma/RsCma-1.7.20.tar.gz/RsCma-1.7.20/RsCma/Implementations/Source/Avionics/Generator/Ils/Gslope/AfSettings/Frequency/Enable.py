from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, freq_1: bool, frequencyLobe=repcap.FrequencyLobe.Default) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:GSLope:AFSettings:FREQuency<nr>:ENABle \n
		Snippet: driver.source.avionics.generator.ils.gslope.afSettings.frequency.enable.set(freq_1 = False, frequencyLobe = repcap.FrequencyLobe.Default) \n
		Enables or disables lobe number <no>. At least one lobe must be enabled. \n
			:param freq_1: OFF | ON
			:param frequencyLobe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frequency')
		"""
		param = Conversions.bool_to_str(freq_1)
		frequencyLobe_cmd_val = self._cmd_group.get_repcap_cmd_value(frequencyLobe, repcap.FrequencyLobe)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:GSLope:AFSettings:FREQuency{frequencyLobe_cmd_val}:ENABle {param}')

	def get(self, frequencyLobe=repcap.FrequencyLobe.Default) -> bool:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:GSLope:AFSettings:FREQuency<nr>:ENABle \n
		Snippet: value: bool = driver.source.avionics.generator.ils.gslope.afSettings.frequency.enable.get(frequencyLobe = repcap.FrequencyLobe.Default) \n
		Enables or disables lobe number <no>. At least one lobe must be enabled. \n
			:param frequencyLobe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frequency')
			:return: freq_1: OFF | ON"""
		frequencyLobe_cmd_val = self._cmd_group.get_repcap_cmd_value(frequencyLobe, repcap.FrequencyLobe)
		response = self._core.io.query_str(f'SOURce:AVIonics:GENerator<Instance>:ILS:GSLope:AFSettings:FREQuency{frequencyLobe_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
