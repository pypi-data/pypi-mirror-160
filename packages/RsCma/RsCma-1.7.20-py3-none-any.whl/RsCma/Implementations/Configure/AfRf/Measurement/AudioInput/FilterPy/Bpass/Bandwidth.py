from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandwidth:
	"""Bandwidth commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bandwidth", core, parent)

	def set(self, bandwidth: float, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:BPASs:BWIDth \n
		Snippet: driver.configure.afRf.measurement.audioInput.filterPy.bpass.bandwidth.set(bandwidth = 1.0, audioInput = repcap.AudioInput.Default) \n
		Configures the bandwidth of the variable bandpass filter in an AF input path. \n
			:param bandwidth: Range: 20 Hz to 20 kHz, Unit: Hz
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.decimal_value_to_str(bandwidth)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:BPASs:BWIDth {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:BPASs:BWIDth \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.filterPy.bpass.bandwidth.get(audioInput = repcap.AudioInput.Default) \n
		Configures the bandwidth of the variable bandpass filter in an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: bandwidth: Range: 20 Hz to 20 kHz, Unit: Hz"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:BPASs:BWIDth?')
		return Conversions.str_to_float(response)
