from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Subnet:
	"""Subnet commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("subnet", core, parent)

	def get_mask(self) -> List[str]:
		"""SCPI: SYSTem:COMMunicate:NET:SUBNet:MASK \n
		Snippet: value: List[str] = driver.system.communicate.net.subnet.get_mask() \n
		Defines the subnet masks to be used for the network adapter. The configuration is only possible if DHCP is disabled.
		A query returns the currently used subnet masks, irrespective of whether they have been assigned manually or via DHCP. \n
			:return: subnet_mask: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NET:SUBNet:MASK?')
		return Conversions.str_to_str_list(response)

	def set_mask(self, subnet_mask: List[str]) -> None:
		"""SCPI: SYSTem:COMMunicate:NET:SUBNet:MASK \n
		Snippet: driver.system.communicate.net.subnet.set_mask(subnet_mask = ['1', '2', '3']) \n
		Defines the subnet masks to be used for the network adapter. The configuration is only possible if DHCP is disabled.
		A query returns the currently used subnet masks, irrespective of whether they have been assigned manually or via DHCP. \n
			:param subnet_mask: String parameter, subnet mask consisting of four blocks separated by dots Several strings separated by commas can be entered, or several masks separated by commas can be included in one string.
		"""
		param = Conversions.list_to_csv_quoted_str(subnet_mask)
		self._core.io.write(f'SYSTem:COMMunicate:NET:SUBNet:MASK {param}')
