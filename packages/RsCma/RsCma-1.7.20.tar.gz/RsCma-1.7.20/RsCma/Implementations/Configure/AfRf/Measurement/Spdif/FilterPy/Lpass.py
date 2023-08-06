from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lpass:
	"""Lpass commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("lpass", core, parent)

	def set(self, filter_left: enums.LowpassFilterExtended, filter_right: enums.LowpassFilterExtended) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:LPASs \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.lpass.set(filter_left = enums.LowpassFilterExtended.F15K, filter_right = enums.LowpassFilterExtended.F15K) \n
		Configures the lowpass filter in the SPDIF input path. \n
			:param filter_left: OFF | F255 | F3K | F3K4 | F4K | F15K Left SPDIF channel
			:param filter_right: OFF | F255 | F3K | F3K4 | F4K | F15K Right SPDIF channel OFF Filter disabled F255, F3K, F3K4, F4K, F15K Cutoff frequency 255 Hz / 3 kHz / 3.4 kHz / 4 kHz / 15 kHz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('filter_left', filter_left, DataType.Enum, enums.LowpassFilterExtended), ArgSingle('filter_right', filter_right, DataType.Enum, enums.LowpassFilterExtended))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:LPASs {param}'.rstrip())

	# noinspection PyTypeChecker
	class LpassStruct(StructBase):
		"""Response structure. Fields: \n
			- Filter_Left: enums.LowpassFilterExtended: OFF | F255 | F3K | F3K4 | F4K | F15K Left SPDIF channel
			- Filter_Right: enums.LowpassFilterExtended: OFF | F255 | F3K | F3K4 | F4K | F15K Right SPDIF channel OFF Filter disabled F255, F3K, F3K4, F4K, F15K Cutoff frequency 255 Hz / 3 kHz / 3.4 kHz / 4 kHz / 15 kHz"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Filter_Left', enums.LowpassFilterExtended),
			ArgStruct.scalar_enum('Filter_Right', enums.LowpassFilterExtended)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Filter_Left: enums.LowpassFilterExtended = None
			self.Filter_Right: enums.LowpassFilterExtended = None

	def get(self) -> LpassStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:LPASs \n
		Snippet: value: LpassStruct = driver.configure.afRf.measurement.spdif.filterPy.lpass.get() \n
		Configures the lowpass filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for LpassStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:LPASs?', self.__class__.LpassStruct())
