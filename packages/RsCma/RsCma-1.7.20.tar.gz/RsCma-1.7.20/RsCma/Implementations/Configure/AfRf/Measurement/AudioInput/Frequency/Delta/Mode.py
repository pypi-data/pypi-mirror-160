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

	def set(self, mode: enums.DeltaMode, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FREQuency:DELTa:MODE \n
		Snippet: driver.configure.afRf.measurement.audioInput.frequency.delta.mode.set(mode = enums.DeltaMode.MEAS, audioInput = repcap.AudioInput.Default) \n
		Configures the AF frequency reference mode. \n
			:param mode: NONE | MEAS | USER
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.DeltaMode)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FREQuency:DELTa:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.DeltaMode:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FREQuency:DELTa:MODE \n
		Snippet: value: enums.DeltaMode = driver.configure.afRf.measurement.audioInput.frequency.delta.mode.get(audioInput = repcap.AudioInput.Default) \n
		Configures the AF frequency reference mode. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: mode: NONE | MEAS | USER"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FREQuency:DELTa:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DeltaMode)
