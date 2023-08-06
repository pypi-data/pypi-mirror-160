from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfOut:
	"""RfOut commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rfOut", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:RFOut:ENABle \n
		Snippet: value: bool = driver.source.avionics.generator.ils.localizer.rfSettings.rfOut.get_enable() \n
		Enables or disables the RF output path for the localizer signal. \n
			:return: rf_enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:RFOut:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, rf_enable: bool) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:RFOut:ENABle \n
		Snippet: driver.source.avionics.generator.ils.localizer.rfSettings.rfOut.set_enable(rf_enable = False) \n
		Enables or disables the RF output path for the localizer signal. \n
			:param rf_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(rf_enable)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:RFOut:ENABle {param}')
