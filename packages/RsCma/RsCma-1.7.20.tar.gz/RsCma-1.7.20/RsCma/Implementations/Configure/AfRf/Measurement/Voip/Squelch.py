from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Squelch:
	"""Squelch commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("squelch", core, parent)

	def get_state(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:SQUelch:STATe \n
		Snippet: value: bool = driver.configure.afRf.measurement.voip.squelch.get_state() \n
		Queries the receiver squelch state in the VoIP path. \n
			:return: state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:SQUelch:STATe?')
		return Conversions.str_to_bool(response)
