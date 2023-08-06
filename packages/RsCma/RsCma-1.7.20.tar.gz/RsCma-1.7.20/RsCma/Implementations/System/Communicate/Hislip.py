from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hislip:
	"""Hislip commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hislip", core, parent)

	def get_vresource(self) -> str:
		"""SCPI: SYSTem:COMMunicate:HISLip:VRESource \n
		Snippet: value: str = driver.system.communicate.hislip.get_vresource() \n
		Queries the VISA resource string for the HiSLIP protocol. \n
			:return: visa_resource: VISA resource string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:HISLip:VRESource?')
		return trim_str_response(response)
