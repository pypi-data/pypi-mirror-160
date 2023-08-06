from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Application:
	"""Application commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("application", core, parent)

	# noinspection PyTypeChecker
	def get_select(self) -> enums.SubTabVseMeas:
		"""SCPI: DISPlay:VSE:MEASurement<Instance>:APPLication:SELect \n
		Snippet: value: enums.SubTabVseMeas = driver.display.vse.measurement.application.get_select() \n
		Configures the display of the subtabs in the 'VSE' tab. \n
			:return: sub_tab: OVERview | RFResults | DEMod | SYMResults | PVTResults | NXDNresults | EYEDiagram | CONStellation | SYMDistr | LTE | SPECtrum
		"""
		response = self._core.io.query_str('DISPlay:VSE:MEASurement<Instance>:APPLication:SELect?')
		return Conversions.str_to_scalar_enum(response, enums.SubTabVseMeas)

	def set_select(self, sub_tab: enums.SubTabVseMeas) -> None:
		"""SCPI: DISPlay:VSE:MEASurement<Instance>:APPLication:SELect \n
		Snippet: driver.display.vse.measurement.application.set_select(sub_tab = enums.SubTabVseMeas.CONStellation) \n
		Configures the display of the subtabs in the 'VSE' tab. \n
			:param sub_tab: OVERview | RFResults | DEMod | SYMResults | PVTResults | NXDNresults | EYEDiagram | CONStellation | SYMDistr | LTE | SPECtrum
		"""
		param = Conversions.enum_scalar_to_str(sub_tab, enums.SubTabVseMeas)
		self._core.io.write(f'DISPlay:VSE:MEASurement<Instance>:APPLication:SELect {param}')
