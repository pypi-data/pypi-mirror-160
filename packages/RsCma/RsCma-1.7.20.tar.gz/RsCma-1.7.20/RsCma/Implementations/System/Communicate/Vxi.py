from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vxi:
	"""Vxi commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vxi", core, parent)

	def get_vresource(self) -> str:
		"""SCPI: SYSTem:COMMunicate:VXI:VRESource \n
		Snippet: value: str = driver.system.communicate.vxi.get_vresource() \n
		Queries the VISA resource string for the VXI-11 protocol. \n
			:return: visa_resource: VISA resource string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:VXI:VRESource?')
		return trim_str_response(response)

	def get_gtr(self) -> bool:
		"""SCPI: SYSTem:COMMunicate:VXI:GTR \n
		Snippet: value: bool = driver.system.communicate.vxi.get_gtr() \n
		No command help available \n
			:return: bool_switchremote: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:VXI:GTR?')
		return Conversions.str_to_bool(response)

	def set_gtr(self, bool_switchremote: bool) -> None:
		"""SCPI: SYSTem:COMMunicate:VXI:GTR \n
		Snippet: driver.system.communicate.vxi.set_gtr(bool_switchremote = False) \n
		No command help available \n
			:param bool_switchremote: No help available
		"""
		param = Conversions.bool_to_str(bool_switchremote)
		self._core.io.write(f'SYSTem:COMMunicate:VXI:GTR {param}')
