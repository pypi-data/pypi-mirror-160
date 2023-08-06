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

	def get_cma(self) -> str:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:CMA \n
		Snippet: value: str = driver.configure.afRf.measurement.voip.uri.get_cma() \n
		Specifies the <user> part of the URI of the R&S CMA180 ('sip:<user>@<IP address>') . \n
			:return: address: String with user part
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:CMA?')
		return trim_str_response(response)

	def set_cma(self, address: str) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:CMA \n
		Snippet: driver.configure.afRf.measurement.voip.uri.set_cma(address = '1') \n
		Specifies the <user> part of the URI of the R&S CMA180 ('sip:<user>@<IP address>') . \n
			:param address: String with user part
		"""
		param = Conversions.value_to_quoted_str(address)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:CMA {param}')

	def get_ip(self) -> str:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:IP \n
		Snippet: value: str = driver.configure.afRf.measurement.voip.uri.get_ip() \n
		Specifies the <IP address> part of the URI of the DUT ('sip:<user>@<IP address>') . \n
			:return: address: IP address as string
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:IP?')
		return trim_str_response(response)

	def set_ip(self, address: str) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:IP \n
		Snippet: driver.configure.afRf.measurement.voip.uri.set_ip(address = '1') \n
		Specifies the <IP address> part of the URI of the DUT ('sip:<user>@<IP address>') . \n
			:param address: IP address as string
		"""
		param = Conversions.value_to_quoted_str(address)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:IP {param}')

	def get_port(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:PORT \n
		Snippet: value: int = driver.configure.afRf.measurement.voip.uri.get_port() \n
		Specifies the URI port number of the DUT. \n
			:return: port: Range: 1024 to 65.535E+3
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:PORT?')
		return Conversions.str_to_int(response)

	def set_port(self, port: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:PORT \n
		Snippet: driver.configure.afRf.measurement.voip.uri.set_port(port = 1) \n
		Specifies the URI port number of the DUT. \n
			:param port: Range: 1024 to 65.535E+3
		"""
		param = Conversions.decimal_value_to_str(port)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:PORT {param}')

	def get_user(self) -> str:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:USER \n
		Snippet: value: str = driver.configure.afRf.measurement.voip.uri.get_user() \n
		Specifies the <user> part of the URI of the DUT ('sip:<user>@<IP address>') . \n
			:return: user: String with user part
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:USER?')
		return trim_str_response(response)

	def set_user(self, user: str) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:USER \n
		Snippet: driver.configure.afRf.measurement.voip.uri.set_user(user = '1') \n
		Specifies the <user> part of the URI of the DUT ('sip:<user>@<IP address>') . \n
			:param user: String with user part
		"""
		param = Conversions.value_to_quoted_str(user)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:URI:USER {param}')
