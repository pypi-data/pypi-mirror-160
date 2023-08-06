from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Socket:
	"""Socket commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("socket", core, parent)

	def get_vresource(self) -> str:
		"""SCPI: SYSTem:COMMunicate:SOCKet:VRESource \n
		Snippet: value: str = driver.system.communicate.socket.get_vresource() \n
		Queries the VISA resource string of the socket resource (direct socket communication) . \n
			:return: visa_resource: VISA resource string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:VRESource?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ProtocolMode:
		"""SCPI: SYSTem:COMMunicate:SOCKet:MODE \n
		Snippet: value: enums.ProtocolMode = driver.system.communicate.socket.get_mode() \n
		Sets the protocol operation mode for direct socket communication. \n
			:return: protocol_mode: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ProtocolMode)

	def set_mode(self, protocol_mode: enums.ProtocolMode) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:MODE \n
		Snippet: driver.system.communicate.socket.set_mode(protocol_mode = enums.ProtocolMode.AGILent) \n
		Sets the protocol operation mode for direct socket communication. \n
			:param protocol_mode: RAW | AGILent | IEEE1174 RAW No support of control messages AGILent Emulation codes via control connection (control port) IEEE1174 Emulation codes via data connection (data port)
		"""
		param = Conversions.enum_scalar_to_str(protocol_mode, enums.ProtocolMode)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:MODE {param}')

	def get_port(self) -> int:
		"""SCPI: SYSTem:COMMunicate:SOCKet:PORT \n
		Snippet: value: int = driver.system.communicate.socket.get_port() \n
		Sets the data port number for direct socket communication. \n
			:return: port_number: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:SOCKet:PORT?')
		return Conversions.str_to_int(response)

	def set_port(self, port_number: int) -> None:
		"""SCPI: SYSTem:COMMunicate:SOCKet:PORT \n
		Snippet: driver.system.communicate.socket.set_port(port_number = 1) \n
		Sets the data port number for direct socket communication. \n
			:param port_number: To select a free port number, enter 0. To select a specific port number, use the following range. Range: 1024 to 32767
		"""
		param = Conversions.decimal_value_to_str(port_number)
		self._core.io.write(f'SYSTem:COMMunicate:SOCKet:PORT {param}')
