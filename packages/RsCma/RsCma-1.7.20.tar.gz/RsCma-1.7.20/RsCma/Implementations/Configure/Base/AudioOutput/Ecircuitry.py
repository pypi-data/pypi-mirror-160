from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ecircuitry:
	"""Ecircuitry commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ecircuitry", core, parent)

	def set(self, circuitry_state: enums.CircuitryState, audioOutput=repcap.AudioOutput.Default) -> None:
		"""SCPI: CONFigure:BASE:AOUT<nr>:ECIRcuitry \n
		Snippet: driver.configure.base.audioOutput.ecircuitry.set(circuitry_state = enums.CircuitryState.ACTive, audioOutput = repcap.AudioOutput.Default) \n
		Selects the set of AF impedance settings to be used. \n
			:param circuitry_state: PASSive | ACTive ACTive: settings for R&S CMA-Z600A (ZBOX commands) PASSive: settings for other equipment (other commands)
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
		"""
		param = Conversions.enum_scalar_to_str(circuitry_state, enums.CircuitryState)
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		self._core.io.write(f'CONFigure:BASE:AOUT{audioOutput_cmd_val}:ECIRcuitry {param}')

	# noinspection PyTypeChecker
	def get(self, audioOutput=repcap.AudioOutput.Default) -> enums.CircuitryState:
		"""SCPI: CONFigure:BASE:AOUT<nr>:ECIRcuitry \n
		Snippet: value: enums.CircuitryState = driver.configure.base.audioOutput.ecircuitry.get(audioOutput = repcap.AudioOutput.Default) \n
		Selects the set of AF impedance settings to be used. \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:return: circuitry_state: PASSive | ACTive ACTive: settings for R&S CMA-Z600A (ZBOX commands) PASSive: settings for other equipment (other commands)"""
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		response = self._core.io.query_str(f'CONFigure:BASE:AOUT{audioOutput_cmd_val}:ECIRcuitry?')
		return Conversions.str_to_scalar_enum(response, enums.CircuitryState)
