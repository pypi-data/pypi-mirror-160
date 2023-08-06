from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sip:
	"""Sip commands group definition. 6 total commands, 0 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sip", core, parent)

	# noinspection PyTypeChecker
	def get_state(self) -> enums.SipState:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:STATe \n
		Snippet: value: enums.SipState = driver.configure.afRf.measurement.voip.sip.get_state() \n
		Queries the state of the VoIP connection to the DUT. \n
			:return: state: TERMinated | ESTablished | ERRor
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.SipState)

	def get_code(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:CODE \n
		Snippet: value: int = driver.configure.afRf.measurement.voip.sip.get_code() \n
		Queries the code number of the last received SIP response. \n
			:return: code: Decimal number, for example 200
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:CODE?')
		return Conversions.str_to_int(response)

	def get_response(self) -> str:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:RESPonse \n
		Snippet: value: str = driver.configure.afRf.measurement.voip.sip.get_response() \n
		Queries the text of the last received SIP response. \n
			:return: response: Response string, for example 'OK'
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:RESPonse?')
		return trim_str_response(response)

	def get_rprotocol(self) -> str:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:RPRotocol \n
		Snippet: value: str = driver.configure.afRf.measurement.voip.sip.get_rprotocol() \n
		Queries information from the reason head field of the SIP. \n
			:return: protocol: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:RPRotocol?')
		return trim_str_response(response)

	def get_rcause(self) -> str:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:RCAuse \n
		Snippet: value: str = driver.configure.afRf.measurement.voip.sip.get_rcause() \n
		Queries information from the reason head field of the SIP. \n
			:return: cause: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:RCAuse?')
		return trim_str_response(response)

	def get_rt_ext(self) -> str:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:RTEXt \n
		Snippet: value: str = driver.configure.afRf.measurement.voip.sip.get_rt_ext() \n
		Queries information from the reason head field of the SIP. \n
			:return: text: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:SIP:RTEXt?')
		return trim_str_response(response)
