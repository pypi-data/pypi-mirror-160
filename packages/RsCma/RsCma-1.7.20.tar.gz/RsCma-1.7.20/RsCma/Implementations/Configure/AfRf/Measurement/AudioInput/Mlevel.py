from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mlevel:
	"""Mlevel commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mlevel", core, parent)

	def set(self, max_level: float, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:MLEVel \n
		Snippet: driver.configure.afRf.measurement.audioInput.mlevel.set(max_level = 1.0, audioInput = repcap.AudioInput.Default) \n
		Specifies the maximum expected level for an AF IN connector in voltage-related units (Table 'Units relevant for remote
		commands') . This setting is only relevant, if auto ranging is disabled. The command sets the same unit for both AF IN
		connectors. If you want to set different level units (e.g. dBm) or set level for both connectors independently, use
		method RsCma.Configure.AfRf.Measurement.AudioInput.First.mlevel for AF1 IN and method RsCma.Configure.AfRf.Measurement.
		AudioInput.Second.mlevel for AF2 IN. \n
			:param max_level: Range: 10E-6 V to 43 V, Unit: V
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.decimal_value_to_str(max_level)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:MLEVel {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:MLEVel \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.mlevel.get(audioInput = repcap.AudioInput.Default) \n
		Specifies the maximum expected level for an AF IN connector in voltage-related units (Table 'Units relevant for remote
		commands') . This setting is only relevant, if auto ranging is disabled. The command sets the same unit for both AF IN
		connectors. If you want to set different level units (e.g. dBm) or set level for both connectors independently, use
		method RsCma.Configure.AfRf.Measurement.AudioInput.First.mlevel for AF1 IN and method RsCma.Configure.AfRf.Measurement.
		AudioInput.Second.mlevel for AF2 IN. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: max_level: Range: 10E-6 V to 43 V, Unit: V"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:MLEVel?')
		return Conversions.str_to_float(response)
