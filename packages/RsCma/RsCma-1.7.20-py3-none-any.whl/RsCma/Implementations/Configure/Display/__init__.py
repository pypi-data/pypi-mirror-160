from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("display", core, parent)

	@property
	def application(self):
		"""application commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_application'):
			from .Application import Application
			self._application = Application(self._core, self._cmd_group)
		return self._application

	# noinspection PyTypeChecker
	def get_tab_split(self) -> enums.TabSplit:
		"""SCPI: CONFigure:DISPlay:TABSplit \n
		Snippet: value: enums.TabSplit = driver.configure.display.get_tab_split() \n
		Configures the tab mode of the GUI. \n
			:return: tab_split: TAB | SPLit TAB Merged mode, displaying a single tab at a time SPLit Split mode, displaying the generator tab on the left and the measurement tabs on the right
		"""
		response = self._core.io.query_str('CONFigure:DISPlay:TABSplit?')
		return Conversions.str_to_scalar_enum(response, enums.TabSplit)

	def set_tab_split(self, tab_split: enums.TabSplit) -> None:
		"""SCPI: CONFigure:DISPlay:TABSplit \n
		Snippet: driver.configure.display.set_tab_split(tab_split = enums.TabSplit.SPLit) \n
		Configures the tab mode of the GUI. \n
			:param tab_split: TAB | SPLit TAB Merged mode, displaying a single tab at a time SPLit Split mode, displaying the generator tab on the left and the measurement tabs on the right
		"""
		param = Conversions.enum_scalar_to_str(tab_split, enums.TabSplit)
		self._core.io.write(f'CONFigure:DISPlay:TABSplit {param}')

	def clone(self) -> 'Display':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Display(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
