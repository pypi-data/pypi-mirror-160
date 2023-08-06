from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hpass:
	"""Hpass commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hpass", core, parent)

	def set(self, filter_py: enums.HighpassFilterExtended, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:HPASs \n
		Snippet: driver.configure.afRf.measurement.audioInput.filterPy.hpass.set(filter_py = enums.HighpassFilterExtended.F300, audioInput = repcap.AudioInput.Default) \n
		Configures the highpass filter in an AF input path. \n
			:param filter_py: OFF | F6 | F50 | F300 OFF Filter disabled F6, F50, F300 Cutoff frequency 6 Hz / 50 Hz / 300 Hz
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(filter_py, enums.HighpassFilterExtended)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:HPASs {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.HighpassFilterExtended:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:HPASs \n
		Snippet: value: enums.HighpassFilterExtended = driver.configure.afRf.measurement.audioInput.filterPy.hpass.get(audioInput = repcap.AudioInput.Default) \n
		Configures the highpass filter in an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: filter_py: OFF | F6 | F50 | F300 OFF Filter disabled F6, F50, F300 Cutoff frequency 6 Hz / 50 Hz / 300 Hz"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:HPASs?')
		return Conversions.str_to_scalar_enum(response, enums.HighpassFilterExtended)
