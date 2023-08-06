from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Types import DataType
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("typePy", core, parent)

	def set(self, filter_type: enums.RbwFilterType, standard: enums.Standard = None) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:FILTer:TYPE \n
		Snippet: driver.configure.vse.measurement.iqRecorder.filterPy.typePy.set(filter_type = enums.RbwFilterType.BANDpass, standard = enums.Standard.CUSTom) \n
		Selects or queries the type of filter to be applied to the data after demodulation and the related digital standard. \n
			:param filter_type: BANDpass | GAUSs
			:param standard: DMR | DPMR | NXDN | P25 | TETRa | LTE | SPECtrum | CUSTom DMR | DPMR | NXDN | P25 | TETRa | LTE Allows query of the filter type, that is a bandpass filter. CUSTom Allows set and query of the filter type.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('filter_type', filter_type, DataType.Enum, enums.RbwFilterType), ArgSingle('standard', standard, DataType.Enum, enums.Standard, is_optional=True))
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:FILTer:TYPE {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self) -> enums.RbwFilterType:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:FILTer:TYPE \n
		Snippet: value: enums.RbwFilterType = driver.configure.vse.measurement.iqRecorder.filterPy.typePy.get() \n
		Selects or queries the type of filter to be applied to the data after demodulation and the related digital standard. \n
			:return: filter_type: BANDpass | GAUSs"""
		response = self._core.io.query_str(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.RbwFilterType)
