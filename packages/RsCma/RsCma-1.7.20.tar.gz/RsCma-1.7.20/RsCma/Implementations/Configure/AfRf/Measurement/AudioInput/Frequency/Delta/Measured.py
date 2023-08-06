from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Measured:
	"""Measured commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("measured", core, parent)

	def get(self, audioInput=repcap.AudioInput.Default) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FREQuency:DELTa:MEASured \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.frequency.delta.measured.get(audioInput = repcap.AudioInput.Default) \n
		Configures the AF frequency measured reference value. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: meas_val: Unit: Hz"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FREQuency:DELTa:MEASured?')
		return Conversions.str_to_float(response)
