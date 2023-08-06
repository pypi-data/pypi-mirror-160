from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lpass:
	"""Lpass commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lpass", core, parent)

	def set(self, filter_py: enums.LowpassFilterExtended, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:LPASs \n
		Snippet: driver.configure.afRf.measurement.audioInput.filterPy.lpass.set(filter_py = enums.LowpassFilterExtended.F15K, audioInput = repcap.AudioInput.Default) \n
		Configures the lowpass filter in an AF input path. \n
			:param filter_py: OFF | F255 | F3K | F3K4 | F4K | F15K OFF Filter disabled F255, F3K, F3K4, F4K, F15K Cutoff frequency 255 Hz / 3 kHz / 3.4 kHz / 4 kHz / 15 kHz
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(filter_py, enums.LowpassFilterExtended)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:LPASs {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.LowpassFilterExtended:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:LPASs \n
		Snippet: value: enums.LowpassFilterExtended = driver.configure.afRf.measurement.audioInput.filterPy.lpass.get(audioInput = repcap.AudioInput.Default) \n
		Configures the lowpass filter in an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: filter_py: OFF | F255 | F3K | F3K4 | F4K | F15K OFF Filter disabled F255, F3K, F3K4, F4K, F15K Cutoff frequency 255 Hz / 3 kHz / 3.4 kHz / 4 kHz / 15 kHz"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:LPASs?')
		return Conversions.str_to_scalar_enum(response, enums.LowpassFilterExtended)
