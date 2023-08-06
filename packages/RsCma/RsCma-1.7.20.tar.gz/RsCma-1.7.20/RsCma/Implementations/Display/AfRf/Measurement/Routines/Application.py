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
	def get_select(self) -> enums.SubTabRoutines:
		"""SCPI: DISPlay:AFRF:MEASurement<Instance>:ROUTines:APPLication:SELect \n
		Snippet: value: enums.SubTabRoutines = driver.display.afRf.measurement.routines.application.get_select() \n
		Configures the display of the subtabs in the 'Routines' tab. \n
			:return: sub_tab: CHARt | TABLe
		"""
		response = self._core.io.query_str('DISPlay:AFRF:MEASurement<Instance>:ROUTines:APPLication:SELect?')
		return Conversions.str_to_scalar_enum(response, enums.SubTabRoutines)

	def set_select(self, sub_tab: enums.SubTabRoutines) -> None:
		"""SCPI: DISPlay:AFRF:MEASurement<Instance>:ROUTines:APPLication:SELect \n
		Snippet: driver.display.afRf.measurement.routines.application.set_select(sub_tab = enums.SubTabRoutines.CHARt) \n
		Configures the display of the subtabs in the 'Routines' tab. \n
			:param sub_tab: CHARt | TABLe
		"""
		param = Conversions.enum_scalar_to_str(sub_tab, enums.SubTabRoutines)
		self._core.io.write(f'DISPlay:AFRF:MEASurement<Instance>:ROUTines:APPLication:SELect {param}')
