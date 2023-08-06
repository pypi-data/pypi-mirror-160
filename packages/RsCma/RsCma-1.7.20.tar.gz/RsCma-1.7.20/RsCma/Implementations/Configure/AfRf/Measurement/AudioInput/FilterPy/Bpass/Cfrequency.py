from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cfrequency:
	"""Cfrequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cfrequency", core, parent)

	def set(self, frequency: float, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:BPASs:CFRequency \n
		Snippet: driver.configure.afRf.measurement.audioInput.filterPy.bpass.cfrequency.set(frequency = 1.0, audioInput = repcap.AudioInput.Default) \n
		Configures the center frequency of the variable bandpass filter in an AF input path. \n
			:param frequency: Range: 0 Hz to 21 kHz, Unit: Hz
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.decimal_value_to_str(frequency)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:BPASs:CFRequency {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:BPASs:CFRequency \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.filterPy.bpass.cfrequency.get(audioInput = repcap.AudioInput.Default) \n
		Configures the center frequency of the variable bandpass filter in an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: frequency: Range: 0 Hz to 21 kHz, Unit: Hz"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:BPASs:CFRequency?')
		return Conversions.str_to_float(response)
