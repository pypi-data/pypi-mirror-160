from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dfrequency:
	"""Dfrequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dfrequency", core, parent)

	def set(self, distor_freq: float, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:DFRequency \n
		Snippet: driver.configure.afRf.measurement.audioInput.filterPy.dfrequency.set(distor_freq = 1.0, audioInput = repcap.AudioInput.Default) \n
		Configures the reference frequency for single-tone measurements via an AF input path. \n
			:param distor_freq: Range: 1 Hz to 10.5 kHz, Unit: Hz
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.decimal_value_to_str(distor_freq)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:DFRequency {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:DFRequency \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.filterPy.dfrequency.get(audioInput = repcap.AudioInput.Default) \n
		Configures the reference frequency for single-tone measurements via an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: distor_freq: Range: 1 Hz to 10.5 kHz, Unit: Hz"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:DFRequency?')
		return Conversions.str_to_float(response)
