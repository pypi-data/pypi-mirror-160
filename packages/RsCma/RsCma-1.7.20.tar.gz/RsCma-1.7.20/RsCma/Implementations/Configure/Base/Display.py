from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("display", core, parent)

	def get_state(self) -> bool:
		"""SCPI: CONFigure:BASE:DISPlay:STATe \n
		Snippet: value: bool = driver.configure.base.display.get_state() \n
		Switches the instrument display off or on. \n
			:return: display_state: OFF | ON OFF: display off (black screen) ON: display on
		"""
		response = self._core.io.query_str('CONFigure:BASE:DISPlay:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, display_state: bool) -> None:
		"""SCPI: CONFigure:BASE:DISPlay:STATe \n
		Snippet: driver.configure.base.display.set_state(display_state = False) \n
		Switches the instrument display off or on. \n
			:param display_state: OFF | ON OFF: display off (black screen) ON: display on
		"""
		param = Conversions.bool_to_str(display_state)
		self._core.io.write(f'CONFigure:BASE:DISPlay:STATe {param}')
