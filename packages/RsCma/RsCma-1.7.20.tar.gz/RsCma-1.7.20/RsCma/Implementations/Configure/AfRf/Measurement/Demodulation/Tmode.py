from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmode:
	"""Tmode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tmode", core, parent)

	def set(self, tone_mode_left: enums.ToneMode, tone_mode_right: enums.ToneMode = None) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:TMODe \n
		Snippet: driver.configure.afRf.measurement.demodulation.tmode.set(tone_mode_left = enums.ToneMode.NOISe, tone_mode_right = enums.ToneMode.NOISe) \n
		No command help available \n
			:param tone_mode_left: No help available
			:param tone_mode_right: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('tone_mode_left', tone_mode_left, DataType.Enum, enums.ToneMode), ArgSingle('tone_mode_right', tone_mode_right, DataType.Enum, enums.ToneMode, is_optional=True))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:TMODe {param}'.rstrip())

	# noinspection PyTypeChecker
	class TmodeStruct(StructBase):
		"""Response structure. Fields: \n
			- Tone_Mode_Left: enums.ToneMode: No parameter help available
			- Tone_Mode_Right: enums.ToneMode: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Tone_Mode_Left', enums.ToneMode),
			ArgStruct.scalar_enum('Tone_Mode_Right', enums.ToneMode)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Tone_Mode_Left: enums.ToneMode = None
			self.Tone_Mode_Right: enums.ToneMode = None

	def get(self) -> TmodeStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:TMODe \n
		Snippet: value: TmodeStruct = driver.configure.afRf.measurement.demodulation.tmode.get() \n
		No command help available \n
			:return: structure: for return value, see the help for TmodeStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:TMODe?', self.__class__.TmodeStruct())
