from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, tone_mode: enums.DigitalToneMode, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN<Nr>:MODE \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.audioInput.mode.set(tone_mode = enums.DigitalToneMode.DCS, audioInput = repcap.AudioInput.Default) \n
		Selects a dialing tone mode for an AF input path. \n
			:param tone_mode: NONE | SELCall | DTMF | FDIA | SCAL None, SelCall, DTMF, free dialing, SELCAL
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(tone_mode, enums.DigitalToneMode)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN{audioInput_cmd_val}:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.DigitalToneMode:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN<Nr>:MODE \n
		Snippet: value: enums.DigitalToneMode = driver.configure.afRf.measurement.multiEval.tones.audioInput.mode.get(audioInput = repcap.AudioInput.Default) \n
		Selects a dialing tone mode for an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: tone_mode: NONE | SELCall | DTMF | FDIA | SCAL None, SelCall, DTMF, free dialing, SELCAL"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:AIN{audioInput_cmd_val}:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DigitalToneMode)
