from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Weighting:
	"""Weighting commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("weighting", core, parent)

	def set(self, filter_left: enums.WeightingFilter, filter_right: enums.WeightingFilter) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:WEIGhting \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.weighting.set(filter_left = enums.WeightingFilter.AWEighting, filter_right = enums.WeightingFilter.AWEighting) \n
		Configures the weighting filter in the SPDIF input path. \n
			:param filter_left: OFF | AWEighting | CCITt | CMESsage Left SPDIF channel OFF Filter disabled AWEighting A-weighting filter CCITt CCITT weighting filter CMESsage C-message weighting filter
			:param filter_right: OFF | AWEighting | CCITt | CMESsage Right SPDIF channel
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('filter_left', filter_left, DataType.Enum, enums.WeightingFilter), ArgSingle('filter_right', filter_right, DataType.Enum, enums.WeightingFilter))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:WEIGhting {param}'.rstrip())

	# noinspection PyTypeChecker
	class WeightingStruct(StructBase):
		"""Response structure. Fields: \n
			- Filter_Left: enums.WeightingFilter: OFF | AWEighting | CCITt | CMESsage Left SPDIF channel OFF Filter disabled AWEighting A-weighting filter CCITt CCITT weighting filter CMESsage C-message weighting filter
			- Filter_Right: enums.WeightingFilter: OFF | AWEighting | CCITt | CMESsage Right SPDIF channel"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Filter_Left', enums.WeightingFilter),
			ArgStruct.scalar_enum('Filter_Right', enums.WeightingFilter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Filter_Left: enums.WeightingFilter = None
			self.Filter_Right: enums.WeightingFilter = None

	def get(self) -> WeightingStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:WEIGhting \n
		Snippet: value: WeightingStruct = driver.configure.afRf.measurement.spdif.filterPy.weighting.get() \n
		Configures the weighting filter in the SPDIF input path. \n
			:return: structure: for return value, see the help for WeightingStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:WEIGhting?', self.__class__.WeightingStruct())
