from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Level:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def set(self, level: float, audioOutput=repcap.AudioOutput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AOUT<nr>:LEVel \n
		Snippet: driver.configure.afRf.measurement.audioOutput.level.set(level = 1.0, audioOutput = repcap.AudioOutput.Default) \n
		Specifies the output level for an AF OUT connector in voltage-related units (Table 'Units relevant for remote commands') .
		The command sets the same unit for both AF OUT connectors. If you want to set different level units (e.g. dBm) or set
		level for both connectors independently, use method RsCma.Configure.AfRf.Measurement.AudioOutput.First.level for AF1 OUT
		and method RsCma.Configure.AfRf.Measurement.AudioOutput.Second.level for AF2 OUT. \n
			:param level: Range: 10E-6 V to 5 V, Unit: V
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
		"""
		param = Conversions.decimal_value_to_str(level)
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AOUT{audioOutput_cmd_val}:LEVel {param}')

	def get(self, audioOutput=repcap.AudioOutput.Default) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AOUT<nr>:LEVel \n
		Snippet: value: float = driver.configure.afRf.measurement.audioOutput.level.get(audioOutput = repcap.AudioOutput.Default) \n
		Specifies the output level for an AF OUT connector in voltage-related units (Table 'Units relevant for remote commands') .
		The command sets the same unit for both AF OUT connectors. If you want to set different level units (e.g. dBm) or set
		level for both connectors independently, use method RsCma.Configure.AfRf.Measurement.AudioOutput.First.level for AF1 OUT
		and method RsCma.Configure.AfRf.Measurement.AudioOutput.Second.level for AF2 OUT. \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:return: level: Range: 10E-6 V to 5 V, Unit: V"""
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AOUT{audioOutput_cmd_val}:LEVel?')
		return Conversions.str_to_float(response)
