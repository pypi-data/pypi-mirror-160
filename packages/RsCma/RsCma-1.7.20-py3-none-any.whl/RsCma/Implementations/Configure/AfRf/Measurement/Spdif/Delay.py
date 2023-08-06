from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	def set(self, audio_delay_left: bool, audio_delay_right: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:DELay \n
		Snippet: driver.configure.afRf.measurement.spdif.delay.set(audio_delay_left = False, audio_delay_right = False) \n
		No command help available \n
			:param audio_delay_left: No help available
			:param audio_delay_right: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('audio_delay_left', audio_delay_left, DataType.Boolean), ArgSingle('audio_delay_right', audio_delay_right, DataType.Boolean))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:DELay {param}'.rstrip())

	# noinspection PyTypeChecker
	class DelayStruct(StructBase):
		"""Response structure. Fields: \n
			- Audio_Delay_Left: bool: No parameter help available
			- Audio_Delay_Right: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Audio_Delay_Left'),
			ArgStruct.scalar_bool('Audio_Delay_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Audio_Delay_Left: bool = None
			self.Audio_Delay_Right: bool = None

	def get(self) -> DelayStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:DELay \n
		Snippet: value: DelayStruct = driver.configure.afRf.measurement.spdif.delay.get() \n
		No command help available \n
			:return: structure: for return value, see the help for DelayStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:DELay?', self.__class__.DelayStruct())
