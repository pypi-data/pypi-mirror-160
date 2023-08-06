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

	def set(self, dwidth: enums.PwrFilterType, relative: enums.Relative) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DWIDth \n
		Snippet: driver.configure.afRf.measurement.voip.filterPy.dwidth.set(dwidth = enums.PwrFilterType.NARRow, relative = enums.Relative.CONStant) \n
		Configures the bandwidth of the distortion filter in the VoIP input path. \n
			:param dwidth: WIDE | NARRow Wide or narrow bandwidth
			:param relative: RELative | CONStant Proportional to reference frequency or constant
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('dwidth', dwidth, DataType.Enum, enums.PwrFilterType), ArgSingle('relative', relative, DataType.Enum, enums.Relative))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DWIDth {param}'.rstrip())

	# noinspection PyTypeChecker
	class DwidthStruct(StructBase):
		"""Response structure. Fields: \n
			- Dwidth: enums.PwrFilterType: WIDE | NARRow Wide or narrow bandwidth
			- Relative: enums.Relative: RELative | CONStant Proportional to reference frequency or constant"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Dwidth', enums.PwrFilterType),
			ArgStruct.scalar_enum('Relative', enums.Relative)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Dwidth: enums.PwrFilterType = None
			self.Relative: enums.Relative = None

	def get(self) -> DwidthStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DWIDth \n
		Snippet: value: DwidthStruct = driver.configure.afRf.measurement.voip.filterPy.dwidth.get() \n
		Configures the bandwidth of the distortion filter in the VoIP input path. \n
			:return: structure: for return value, see the help for DwidthStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FILTer:DWIDth?', self.__class__.DwidthStruct())
