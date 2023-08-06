from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmode:
	"""Tmode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tmode", core, parent)

	def set(self, tone_mode: enums.ToneMode, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:TMODe \n
		Snippet: driver.configure.afRf.measurement.audioInput.tmode.set(tone_mode = enums.ToneMode.NOISe, audioInput = repcap.AudioInput.Default) \n
		No command help available \n
			:param tone_mode: No help available
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(tone_mode, enums.ToneMode)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:TMODe {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.ToneMode:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:TMODe \n
		Snippet: value: enums.ToneMode = driver.configure.afRf.measurement.audioInput.tmode.get(audioInput = repcap.AudioInput.Default) \n
		No command help available \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: tone_mode: No help available"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ToneMode)
