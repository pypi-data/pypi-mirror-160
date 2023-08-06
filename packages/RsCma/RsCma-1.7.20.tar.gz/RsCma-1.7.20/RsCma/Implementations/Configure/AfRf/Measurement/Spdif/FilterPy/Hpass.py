from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Hpass:
	"""Hpass commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hpass", core, parent)

	def set(self, filter_left: enums.HighpassFilterExtended, filter_right: enums.HighpassFilterExtended) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:HPASs \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.hpass.set(filter_left = enums.HighpassFilterExtended.F300, filter_right = enums.HighpassFilterExtended.F300) \n
		Configures the highpass filter in the SPDIF input path. \n
			:param filter_left: OFF | F6 | F50 | F300 Left SPDIF channel OFF Filter disabled F6, F50, F300 Cutoff frequency 6 Hz / 50 Hz / 300 Hz
			:param filter_right: OFF | F6 | F50 | F300 Right SPDIF channel
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('filter_left', filter_left, DataType.Enum, enums.HighpassFilterExtended), ArgSingle('filter_right', filter_right, DataType.Enum, enums.HighpassFilterExtended))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:HPASs {param}'.rstrip())

	# noinspection PyTypeChecker
	class HpassStruct(StructBase):
		"""Response structure. Fields: \n
			- Filter_Left: enums.HighpassFilterExtended: OFF | F6 | F50 | F300 Left SPDIF channel OFF Filter disabled F6, F50, F300 Cutoff frequency 6 Hz / 50 Hz / 300 Hz
			- Filter_Right: enums.HighpassFilterExtended: OFF | F6 | F50 | F300 Right SPDIF channel"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Filter_Left', enums.HighpassFilterExtended),
			ArgStruct.scalar_enum('Filter_Right', enums.HighpassFilterExtended)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Filter_Left: enums.HighpassFilterExtended = None
			self.Filter_Right: enums.HighpassFilterExtended = None

	def get(self) -> HpassStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:HPASs \n
		Snippet: value: HpassStruct = driver.configure.afRf.measurement.spdif.filterPy.hpass.get() \n
		Configures the highpass filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for HpassStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:HPASs?', self.__class__.HpassStruct())
