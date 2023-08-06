from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Attenuator:
	"""Attenuator commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("attenuator", core, parent)

	def set(self, enable: bool, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:BASE:AIN<nr>:ZBOX:ATTenuator \n
		Snippet: driver.configure.base.audioInput.zbox.attenuator.set(enable = False, audioInput = repcap.AudioInput.Default) \n
		Specifies whether the AF IN attenuator in the impedance matching unit is on or off. \n
			:param enable: OFF | ON Attenuator state
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.bool_to_str(enable)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:BASE:AIN{audioInput_cmd_val}:ZBOX:ATTenuator {param}')

	def get(self, audioInput=repcap.AudioInput.Default) -> bool:
		"""SCPI: CONFigure:BASE:AIN<nr>:ZBOX:ATTenuator \n
		Snippet: value: bool = driver.configure.base.audioInput.zbox.attenuator.get(audioInput = repcap.AudioInput.Default) \n
		Specifies whether the AF IN attenuator in the impedance matching unit is on or off. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: enable: OFF | ON Attenuator state"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:BASE:AIN{audioInput_cmd_val}:ZBOX:ATTenuator?')
		return Conversions.str_to_bool(response)
