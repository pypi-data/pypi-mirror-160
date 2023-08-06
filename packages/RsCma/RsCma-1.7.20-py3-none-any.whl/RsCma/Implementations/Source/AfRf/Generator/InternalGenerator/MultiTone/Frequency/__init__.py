from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	@property
	def auto(self):
		"""auto commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_auto'):
			from .Auto import Auto
			self._auto = Auto(self._core, self._cmd_group)
		return self._auto

	def set(self, frequency: List[float], internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:FREQuency \n
		Snippet: driver.source.afRf.generator.internalGenerator.multiTone.frequency.set(frequency = [1.1, 2.2, 3.3], internalGen = repcap.InternalGen.Default) \n
		Configures the frequencies of a multitone signal. \n
			:param frequency: Comma-separated list of up to 20 frequencies, tone 1 to tone 20 You can specify fewer than 20 values to configure only the beginning of the tone list. Range: 20 Hz to 21 kHz, Unit: Hz
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
		"""
		param = Conversions.list_to_csv_str(frequency)
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:FREQuency {param}')

	def get(self, internalGen=repcap.InternalGen.Default) -> List[float]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:FREQuency \n
		Snippet: value: List[float] = driver.source.afRf.generator.internalGenerator.multiTone.frequency.get(internalGen = repcap.InternalGen.Default) \n
		Configures the frequencies of a multitone signal. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: frequency: Comma-separated list of up to 20 frequencies, tone 1 to tone 20 You can specify fewer than 20 values to configure only the beginning of the tone list. Range: 20 Hz to 21 kHz, Unit: Hz"""
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		response = self._core.io.query_bin_or_ascii_float_list(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:FREQuency?')
		return response

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
