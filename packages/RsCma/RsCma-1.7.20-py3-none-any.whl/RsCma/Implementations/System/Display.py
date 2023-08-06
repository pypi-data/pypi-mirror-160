from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("display", core, parent)

	def get_update(self) -> bool:
		"""SCPI: SYSTem:DISPlay:UPDate \n
		Snippet: value: bool = driver.system.display.get_update() \n
		Defines whether the display is updated or not while the instrument is in the remote state. Disabling the update speeds up
		testing and is the recommended state. See also 'Using the display during remote control'. \n
			:return: display_update: No help available
		"""
		response = self._core.io.query_str('SYSTem:DISPlay:UPDate?')
		return Conversions.str_to_bool(response)

	def set_update(self, display_update: bool) -> None:
		"""SCPI: SYSTem:DISPlay:UPDate \n
		Snippet: driver.system.display.set_update(display_update = False) \n
		Defines whether the display is updated or not while the instrument is in the remote state. Disabling the update speeds up
		testing and is the recommended state. See also 'Using the display during remote control'. \n
			:param display_update: 1 | 0 1: The display is shown and updated during remote control. 0: The display shows static image during remote control.
		"""
		param = Conversions.bool_to_str(display_update)
		self._core.io.write(f'SYSTem:DISPlay:UPDate {param}')
