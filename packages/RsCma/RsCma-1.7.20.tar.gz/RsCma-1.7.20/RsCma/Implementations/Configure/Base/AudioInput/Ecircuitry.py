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

	def set(self, circuitry_state: enums.CircuitryState, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:BASE:AIN<nr>:ECIRcuitry \n
		Snippet: driver.configure.base.audioInput.ecircuitry.set(circuitry_state = enums.CircuitryState.ACTive, audioInput = repcap.AudioInput.Default) \n
		Selects the set of AF impedance settings to be used. \n
			:param circuitry_state: PASSive | ACTive ACTive: settings for R&S CMA-Z600A (ZBOX commands) PASSive: settings for other equipment (other commands)
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(circuitry_state, enums.CircuitryState)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:BASE:AIN{audioInput_cmd_val}:ECIRcuitry {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.CircuitryState:
		"""SCPI: CONFigure:BASE:AIN<nr>:ECIRcuitry \n
		Snippet: value: enums.CircuitryState = driver.configure.base.audioInput.ecircuitry.get(audioInput = repcap.AudioInput.Default) \n
		Selects the set of AF impedance settings to be used. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: circuitry_state: PASSive | ACTive ACTive: settings for R&S CMA-Z600A (ZBOX commands) PASSive: settings for other equipment (other commands)"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:BASE:AIN{audioInput_cmd_val}:ECIRcuitry?')
		return Conversions.str_to_scalar_enum(response, enums.CircuitryState)
