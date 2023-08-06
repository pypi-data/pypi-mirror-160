from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dwidth:
	"""Dwidth commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dwidth", core, parent)

	def set(self, dwidth_left: enums.PwrFilterType, relative_left: enums.Relative, dwidth_right: enums.PwrFilterType, relative_right: enums.Relative) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DWIDth \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.dwidth.set(dwidth_left = enums.PwrFilterType.NARRow, relative_left = enums.Relative.CONStant, dwidth_right = enums.PwrFilterType.NARRow, relative_right = enums.Relative.CONStant) \n
		Configures the bandwidth of the distortion filter in the RF input path. For FM stereo, the settings configure the left
		and the right audio channel. For other modulation types, only the <...Left> settings are relevant. The <...
		Right> settings have no effect. \n
			:param dwidth_left: WIDE | NARRow Wide or narrow bandwidth
			:param relative_left: RELative | CONStant Bandwidth proportional to reference frequency or constant
			:param dwidth_right: WIDE | NARRow
			:param relative_right: RELative | CONStant
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('dwidth_left', dwidth_left, DataType.Enum, enums.PwrFilterType), ArgSingle('relative_left', relative_left, DataType.Enum, enums.Relative), ArgSingle('dwidth_right', dwidth_right, DataType.Enum, enums.PwrFilterType), ArgSingle('relative_right', relative_right, DataType.Enum, enums.Relative))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DWIDth {param}'.rstrip())

	# noinspection PyTypeChecker
	class DwidthStruct(StructBase):
		"""Response structure. Fields: \n
			- Dwidth_Left: enums.PwrFilterType: WIDE | NARRow Wide or narrow bandwidth
			- Relative_Left: enums.Relative: RELative | CONStant Bandwidth proportional to reference frequency or constant
			- Dwidth_Right: enums.PwrFilterType: WIDE | NARRow
			- Relative_Right: enums.Relative: RELative | CONStant"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Dwidth_Left', enums.PwrFilterType),
			ArgStruct.scalar_enum('Relative_Left', enums.Relative),
			ArgStruct.scalar_enum('Dwidth_Right', enums.PwrFilterType),
			ArgStruct.scalar_enum('Relative_Right', enums.Relative)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dwidth_Left: enums.PwrFilterType = None
			self.Relative_Left: enums.Relative = None
			self.Dwidth_Right: enums.PwrFilterType = None
			self.Relative_Right: enums.Relative = None

	def get(self) -> DwidthStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DWIDth \n
		Snippet: value: DwidthStruct = driver.configure.afRf.measurement.demodulation.filterPy.dwidth.get() \n
		Configures the bandwidth of the distortion filter in the RF input path. For FM stereo, the settings configure the left
		and the right audio channel. For other modulation types, only the <...Left> settings are relevant. The <...
		Right> settings have no effect. \n
			:return: structure: for return value, see the help for DwidthStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:DWIDth?', self.__class__.DwidthStruct())
