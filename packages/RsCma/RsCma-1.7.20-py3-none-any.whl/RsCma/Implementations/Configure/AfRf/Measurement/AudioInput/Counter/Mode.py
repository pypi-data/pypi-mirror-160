from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, freq_counter_mode: enums.FreqCounterMode, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:COUNter:MODE \n
		Snippet: driver.configure.afRf.measurement.audioInput.counter.mode.set(freq_counter_mode = enums.FreqCounterMode.HW, audioInput = repcap.AudioInput.Default) \n
		Selects the type of frequency counter for measuring the AF frequency. \n
			:param freq_counter_mode: SW | HW Software or hardware implementation of the frequency counter
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(freq_counter_mode, enums.FreqCounterMode)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:COUNter:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.FreqCounterMode:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:COUNter:MODE \n
		Snippet: value: enums.FreqCounterMode = driver.configure.afRf.measurement.audioInput.counter.mode.get(audioInput = repcap.AudioInput.Default) \n
		Selects the type of frequency counter for measuring the AF frequency. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: freq_counter_mode: SW | HW Software or hardware implementation of the frequency counter"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:COUNter:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FreqCounterMode)
