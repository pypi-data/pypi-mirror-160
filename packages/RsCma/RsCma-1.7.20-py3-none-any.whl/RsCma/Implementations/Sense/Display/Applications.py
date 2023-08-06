from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Applications:
	"""Applications commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("applications", core, parent)

	def get_catalog(self) -> List[str]:
		"""SCPI: SENSe:DISPlay:APPLications:CATalog \n
		Snippet: value: List[str] = driver.sense.display.applications.get_catalog() \n
		Queries a list of all applications available in the current scenario. \n
			:return: app_list: Comma-separated list of strings, each string indicating one application, for example 'Generator' or 'Analyzer'
		"""
		response = self._core.io.query_str('SENSe:DISPlay:APPLications:CATalog?')
		return Conversions.str_to_str_list(response)
