from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rsib:
	"""Rsib commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rsib", core, parent)

	def get_vresource(self) -> str:
		"""SCPI: SYSTem:COMMunicate:RSIB:VRESource \n
		Snippet: value: str = driver.system.communicate.rsib.get_vresource() \n
		No command help available \n
			:return: visa_resource: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:RSIB:VRESource?')
		return trim_str_response(response)
