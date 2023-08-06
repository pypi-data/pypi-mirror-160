from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limpedance:
	"""Limpedance commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("limpedance", core, parent)

	def set(self, enable: bool, impedance: float, audioOutput=repcap.AudioOutput.Default) -> None:
		"""SCPI: CONFigure:BASE:AOUT<nr>:LIMPedance \n
		Snippet: driver.configure.base.audioOutput.limpedance.set(enable = False, impedance = 1.0, audioOutput = repcap.AudioOutput.Default) \n
		Configures the impedance 'R Load'. \n
			:param enable: OFF | ON ON: Use the configured Impedance. OFF: Ignore the configured Impedance.
			:param impedance: Range: 1 Ω to 100E+6 Ω, Unit: Ω
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('impedance', impedance, DataType.Float))
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		self._core.io.write(f'CONFigure:BASE:AOUT{audioOutput_cmd_val}:LIMPedance {param}'.rstrip())

	# noinspection PyTypeChecker
	class LimpedanceStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON ON: Use the configured Impedance. OFF: Ignore the configured Impedance.
			- Impedance: float: Range: 1 Ω to 100E+6 Ω, Unit: Ω"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Impedance')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Impedance: float = None

	def get(self, audioOutput=repcap.AudioOutput.Default) -> LimpedanceStruct:
		"""SCPI: CONFigure:BASE:AOUT<nr>:LIMPedance \n
		Snippet: value: LimpedanceStruct = driver.configure.base.audioOutput.limpedance.get(audioOutput = repcap.AudioOutput.Default) \n
		Configures the impedance 'R Load'. \n
			:param audioOutput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioOutput')
			:return: structure: for return value, see the help for LimpedanceStruct structure arguments."""
		audioOutput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioOutput, repcap.AudioOutput)
		return self._core.io.query_struct(f'CONFigure:BASE:AOUT{audioOutput_cmd_val}:LIMPedance?', self.__class__.LimpedanceStruct())
