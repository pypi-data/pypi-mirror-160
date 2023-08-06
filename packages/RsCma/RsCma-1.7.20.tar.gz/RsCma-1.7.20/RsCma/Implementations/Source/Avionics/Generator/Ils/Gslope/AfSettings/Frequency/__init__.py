from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.RepeatedCapability import RepeatedCapability
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 1 Subgroups, 1 group commands
	Repeated Capability: FrequencyLobe, default value after init: FrequencyLobe.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_frequencyLobe_get', 'repcap_frequencyLobe_set', repcap.FrequencyLobe.Nr1)

	def repcap_frequencyLobe_set(self, frequencyLobe: repcap.FrequencyLobe) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to FrequencyLobe.Default
		Default value after init: FrequencyLobe.Nr1"""
		self._cmd_group.set_repcap_enum_value(frequencyLobe)

	def repcap_frequencyLobe_get(self) -> repcap.FrequencyLobe:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import Enable
			self._enable = Enable(self._core, self._cmd_group)
		return self._enable

	def set(self, freq_1: int, frequencyLobe=repcap.FrequencyLobe.Default) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:GSLope:AFSettings:FREQuency<nr> \n
		Snippet: driver.source.avionics.generator.ils.gslope.afSettings.frequency.set(freq_1 = 1, frequencyLobe = repcap.FrequencyLobe.Default) \n
		Configures the audio frequency for one lobe. \n
			:param freq_1: Range and reset value depend on no Range: 72 Hz to 108 Hz / 120 Hz to 180 Hz , Unit: Hz
			:param frequencyLobe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frequency')
		"""
		param = Conversions.decimal_value_to_str(freq_1)
		frequencyLobe_cmd_val = self._cmd_group.get_repcap_cmd_value(frequencyLobe, repcap.FrequencyLobe)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:GSLope:AFSettings:FREQuency{frequencyLobe_cmd_val} {param}')

	def get(self, frequencyLobe=repcap.FrequencyLobe.Default) -> int:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:GSLope:AFSettings:FREQuency<nr> \n
		Snippet: value: int = driver.source.avionics.generator.ils.gslope.afSettings.frequency.get(frequencyLobe = repcap.FrequencyLobe.Default) \n
		Configures the audio frequency for one lobe. \n
			:param frequencyLobe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frequency')
			:return: freq_1: Range and reset value depend on no Range: 72 Hz to 108 Hz / 120 Hz to 180 Hz , Unit: Hz"""
		frequencyLobe_cmd_val = self._cmd_group.get_repcap_cmd_value(frequencyLobe, repcap.FrequencyLobe)
		response = self._core.io.query_str(f'SOURce:AVIonics:GENerator<Instance>:ILS:GSLope:AFSettings:FREQuency{frequencyLobe_cmd_val}?')
		return Conversions.str_to_int(response)

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
