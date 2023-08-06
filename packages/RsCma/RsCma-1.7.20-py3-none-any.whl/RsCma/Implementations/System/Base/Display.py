from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("display", core, parent)

	# noinspection PyTypeChecker
	def get_language(self) -> enums.DisplayLanguage:
		"""SCPI: SYSTem:BASE:DISPlay:LANGuage \n
		Snippet: value: enums.DisplayLanguage = driver.system.base.display.get_language() \n
		Selects the GUI language to be used. The corresponding language and license must be installed. \n
			:return: language: AR | DE | SV | RU | KO | JA | EN | IT | FR | DA | ES | TR | CS | ZH
		"""
		response = self._core.io.query_str('SYSTem:BASE:DISPlay:LANGuage?')
		return Conversions.str_to_scalar_enum(response, enums.DisplayLanguage)

	def set_language(self, language: enums.DisplayLanguage) -> None:
		"""SCPI: SYSTem:BASE:DISPlay:LANGuage \n
		Snippet: driver.system.base.display.set_language(language = enums.DisplayLanguage.AR) \n
		Selects the GUI language to be used. The corresponding language and license must be installed. \n
			:param language: AR | DE | SV | RU | KO | JA | EN | IT | FR | DA | ES | TR | CS | ZH
		"""
		param = Conversions.enum_scalar_to_str(language, enums.DisplayLanguage)
		self._core.io.write(f'SYSTem:BASE:DISPlay:LANGuage {param}')
