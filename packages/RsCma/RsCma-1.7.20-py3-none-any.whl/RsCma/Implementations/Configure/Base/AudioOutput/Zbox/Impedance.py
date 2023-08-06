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

	def set(self, impedance: enums.Impedance, audioOutput=repcap.AudioOutput.Default) -> None:
		"""SCPI: CONFigure:BASE:AOUT<nr>:ZBOX:IMPedance \n
		Snippet: driver.configure.base.audioOutput.zbox.impedance.set(impedance = enums.Impedance.IHOL, audioOutput = repcap.AudioOutput.Default) \n
		Specifies the impedance that is configured at the impedance matching unit. \n
			:param impedance: IHOL | R50 | R150 | R300 | R600 IHOL In high / out low R50 | R150 | R300 | R600 50 Ω | 150 Ω | 300 Ω | 600 Ω
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.Impedance)
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		self._core.io.write(f'CONFigure:BASE:AOUT{audioOutput_cmd_val}:ZBOX:IMPedance {param}')

	# noinspection PyTypeChecker
	def get(self, audioOutput=repcap.AudioOutput.Default) -> enums.Impedance:
		"""SCPI: CONFigure:BASE:AOUT<nr>:ZBOX:IMPedance \n
		Snippet: value: enums.Impedance = driver.configure.base.audioOutput.zbox.impedance.get(audioOutput = repcap.AudioOutput.Default) \n
		Specifies the impedance that is configured at the impedance matching unit. \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:return: impedance: IHOL | R50 | R150 | R300 | R600 IHOL In high / out low R50 | R150 | R300 | R600 50 Ω | 150 Ω | 300 Ω | 600 Ω"""
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		response = self._core.io.query_str(f'CONFigure:BASE:AOUT{audioOutput_cmd_val}:ZBOX:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.Impedance)
