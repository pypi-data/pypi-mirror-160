from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uri:
	"""Uri commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("uri", core, parent)

	def get_port(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:URI:PORT \n
		Snippet: value: int = driver.source.afRf.generator.voip.uri.get_port() \n
		Specifies the URI port number of the DUT. \n
			:return: port: Range: 1024 to 65.535E+3
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:URI:PORT?')
		return Conversions.str_to_int(response)

	def set_port(self, port: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:URI:PORT \n
		Snippet: driver.source.afRf.generator.voip.uri.set_port(port = 1) \n
		Specifies the URI port number of the DUT. \n
			:param port: Range: 1024 to 65.535E+3
		"""
		param = Conversions.decimal_value_to_str(port)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:VOIP:URI:PORT {param}')

	def get_cma(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:URI:CMA \n
		Snippet: value: str = driver.source.afRf.generator.voip.uri.get_cma() \n
		Specifies the <user> part of the URI of the R&S CMA180 ('sip:<user>@<IP address>') . \n
			:return: cma_uri: String with user part
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:URI:CMA?')
		return trim_str_response(response)

	def set_cma(self, cma_uri: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:URI:CMA \n
		Snippet: driver.source.afRf.generator.voip.uri.set_cma(cma_uri = '1') \n
		Specifies the <user> part of the URI of the R&S CMA180 ('sip:<user>@<IP address>') . \n
			:param cma_uri: String with user part
		"""
		param = Conversions.value_to_quoted_str(cma_uri)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:VOIP:URI:CMA {param}')

	def get_ip(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:URI:IP \n
		Snippet: value: str = driver.source.afRf.generator.voip.uri.get_ip() \n
		Specifies the <IP address> part of the URI of the DUT ('sip:<user>@<IP address>') . \n
			:return: uri_ip: IP address as string
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:URI:IP?')
		return trim_str_response(response)

	def set_ip(self, uri_ip: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:URI:IP \n
		Snippet: driver.source.afRf.generator.voip.uri.set_ip(uri_ip = '1') \n
		Specifies the <IP address> part of the URI of the DUT ('sip:<user>@<IP address>') . \n
			:param uri_ip: IP address as string
		"""
		param = Conversions.value_to_quoted_str(uri_ip)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:VOIP:URI:IP {param}')

	def get_user(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:URI:USER \n
		Snippet: value: str = driver.source.afRf.generator.voip.uri.get_user() \n
		Specifies the <user> part of the URI of the DUT ('sip:<user>@<IP address>') . \n
			:return: uri_user: String with user part
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:VOIP:URI:USER?')
		return trim_str_response(response)

	def set_user(self, uri_user: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:VOIP:URI:USER \n
		Snippet: driver.source.afRf.generator.voip.uri.set_user(uri_user = '1') \n
		Specifies the <user> part of the URI of the DUT ('sip:<user>@<IP address>') . \n
			:param uri_user: String with user part
		"""
		param = Conversions.value_to_quoted_str(uri_user)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:VOIP:URI:USER {param}')
