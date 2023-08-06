from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("user", core, parent)

	def set(self, user_val: float, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FREQuency:DELTa:USER \n
		Snippet: driver.configure.afRf.measurement.audioInput.frequency.delta.user.set(user_val = 1.0, audioInput = repcap.AudioInput.Default) \n
		Configures the AF frequency user reference value. \n
			:param user_val: Unit: Hz
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.decimal_value_to_str(user_val)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FREQuency:DELTa:USER {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FREQuency:DELTa:USER \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.frequency.delta.user.get(audioInput = repcap.AudioInput.Default) \n
		Configures the AF frequency user reference value. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: user_val: Unit: Hz"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FREQuency:DELTa:USER?')
		return Conversions.str_to_float(response)
