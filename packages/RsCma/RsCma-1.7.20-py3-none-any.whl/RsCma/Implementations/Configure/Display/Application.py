from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Application:
	"""Application commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("application", core, parent)

	def get_select(self) -> str:
		"""SCPI: CONFigure:DISPlay:APPLication:SELect \n
		Snippet: value: str = driver.configure.display.application.get_select() \n
		Selects the application to be displayed at the GUI. The command is useful as preparation for taking screenshots via
		remote commands. To make the GUI visible during remote control, use the command method RsCma.System.Display.update.
		To query a list of application selection strings, see method RsCma.Sense.Display.Applications.catalog. \n
			:return: current_app: String selecting the application
		"""
		response = self._core.io.query_str('CONFigure:DISPlay:APPLication:SELect?')
		return trim_str_response(response)

	def set_select(self, current_app: str) -> None:
		"""SCPI: CONFigure:DISPlay:APPLication:SELect \n
		Snippet: driver.configure.display.application.set_select(current_app = '1') \n
		Selects the application to be displayed at the GUI. The command is useful as preparation for taking screenshots via
		remote commands. To make the GUI visible during remote control, use the command method RsCma.System.Display.update.
		To query a list of application selection strings, see method RsCma.Sense.Display.Applications.catalog. \n
			:param current_app: String selecting the application
		"""
		param = Conversions.value_to_quoted_str(current_app)
		self._core.io.write(f'CONFigure:DISPlay:APPLication:SELect {param}')
