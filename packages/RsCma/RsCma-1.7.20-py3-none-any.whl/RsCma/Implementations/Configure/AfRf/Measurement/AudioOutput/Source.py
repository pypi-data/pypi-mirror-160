from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("source", core, parent)

	def set(self, audioOutput=repcap.AudioOutput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AOUT<nr>:SOURce \n
		Snippet: driver.configure.afRf.measurement.audioOutput.source.set(audioOutput = repcap.AudioOutput.Default) \n
		Sets the audio signal source for an AF OUT connector. \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
		"""
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AOUT{audioOutput_cmd_val}:SOURce')

	def set_with_opc(self, audioOutput=repcap.AudioOutput.Default, opc_timeout_ms: int = -1) -> None:
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AOUT<nr>:SOURce \n
		Snippet: driver.configure.afRf.measurement.audioOutput.source.set_with_opc(audioOutput = repcap.AudioOutput.Default) \n
		Sets the audio signal source for an AF OUT connector. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:AFRF:MEASurement<Instance>:AOUT{audioOutput_cmd_val}:SOURce', opc_timeout_ms)

	# noinspection PyTypeChecker
	def get(self, audioOutput=repcap.AudioOutput.Default) -> enums.AudioSource:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AOUT<nr>:SOURce \n
		Snippet: value: enums.AudioSource = driver.configure.afRf.measurement.audioOutput.source.get(audioOutput = repcap.AudioOutput.Default) \n
		Sets the audio signal source for an AF OUT connector. \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:return: source: NONE | DEM | DEML | DEMR | VOIP | UGEN DEM Demodulator output (FM, PM, ...) DEML Demodulator output, left channel (FM stereo) DEMR Demodulator output, right channel (FM stereo) VOIP Generated audio signal transported via LAN (VoIP) UGEN User-generated audio signal"""
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AOUT{audioOutput_cmd_val}:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.AudioSource)
