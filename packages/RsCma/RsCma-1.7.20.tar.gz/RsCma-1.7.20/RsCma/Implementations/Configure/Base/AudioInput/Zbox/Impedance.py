from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Impedance:
	"""Impedance commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("impedance", core, parent)

	def set(self, impedance: enums.Impedance, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:BASE:AIN<nr>:ZBOX:IMPedance \n
		Snippet: driver.configure.base.audioInput.zbox.impedance.set(impedance = enums.Impedance.IHOL, audioInput = repcap.AudioInput.Default) \n
		Specifies the impedance that is configured at the impedance matching unit. \n
			:param impedance: IHOL | R50 | R150 | R300 | R600 IHOL In high / out low R50 | R150 | R300 | R600 50 Ω | 150 Ω | 300 Ω | 600 Ω
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.Impedance)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:BASE:AIN{audioInput_cmd_val}:ZBOX:IMPedance {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.Impedance:
		"""SCPI: CONFigure:BASE:AIN<nr>:ZBOX:IMPedance \n
		Snippet: value: enums.Impedance = driver.configure.base.audioInput.zbox.impedance.get(audioInput = repcap.AudioInput.Default) \n
		Specifies the impedance that is configured at the impedance matching unit. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: impedance: IHOL | R50 | R150 | R300 | R600 IHOL In high / out low R50 | R150 | R300 | R600 50 Ω | 150 Ω | 300 Ω | 600 Ω"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:BASE:AIN{audioInput_cmd_val}:ZBOX:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.Impedance)
