from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dns:
	"""Dns commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dns", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SYSTem:COMMunicate:NET:DNS:ENABle \n
		Snippet: value: bool = driver.system.communicate.net.dns.get_enable() \n
		Enables or disables the configuration of DNS addresses via DHCP. \n
			:return: dns_enable: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:NET:DNS:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, dns_enable: bool) -> None:
		"""SCPI: SYSTem:COMMunicate:NET:DNS:ENABle \n
		Snippet: driver.system.communicate.net.dns.set_enable(dns_enable = False) \n
		Enables or disables the configuration of DNS addresses via DHCP. \n
			:param dns_enable: 1 | 0 1: Enabled, automatic address configuration 0: Disabled, manual address configuration
		"""
		param = Conversions.bool_to_str(dns_enable)
		self._core.io.write(f'SYSTem:COMMunicate:NET:DNS:ENABle {param}')
