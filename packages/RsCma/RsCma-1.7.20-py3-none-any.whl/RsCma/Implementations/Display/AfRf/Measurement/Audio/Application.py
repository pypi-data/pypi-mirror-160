from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Application:
	"""Application commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("application", core, parent)

	# noinspection PyTypeChecker
	def get_select(self) -> enums.SubTabAudioMeas:
		"""SCPI: DISPlay:AFRF:MEASurement<Instance>:AUDio:APPLication:SELect \n
		Snippet: value: enums.SubTabAudioMeas = driver.display.afRf.measurement.audio.application.get_select() \n
		Configures the display of the subtabs in the 'Audio' tab. \n
			:return: sub_tab: OVERview | TRIM | AFResults | FFT | OSC
		"""
		response = self._core.io.query_str('DISPlay:AFRF:MEASurement<Instance>:AUDio:APPLication:SELect?')
		return Conversions.str_to_scalar_enum(response, enums.SubTabAudioMeas)

	def set_select(self, sub_tab: enums.SubTabAudioMeas) -> None:
		"""SCPI: DISPlay:AFRF:MEASurement<Instance>:AUDio:APPLication:SELect \n
		Snippet: driver.display.afRf.measurement.audio.application.set_select(sub_tab = enums.SubTabAudioMeas.AFResults) \n
		Configures the display of the subtabs in the 'Audio' tab. \n
			:param sub_tab: OVERview | TRIM | AFResults | FFT | OSC
		"""
		param = Conversions.enum_scalar_to_str(sub_tab, enums.SubTabAudioMeas)
		self._core.io.write(f'DISPlay:AFRF:MEASurement<Instance>:AUDio:APPLication:SELect {param}')
