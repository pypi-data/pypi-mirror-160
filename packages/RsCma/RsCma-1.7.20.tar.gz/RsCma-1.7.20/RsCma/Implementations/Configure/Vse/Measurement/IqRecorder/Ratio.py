from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ratio:
	"""Ratio commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ratio", core, parent)

	def set(self, ratio: float, standard: enums.Standard = None) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:RATio \n
		Snippet: driver.configure.vse.measurement.iqRecorder.ratio.set(ratio = 1.0, standard = enums.Standard.CUSTom) \n
		Sets or queries the ratio of 'Sample Rate' and 'Max. Sample Rate'. \n
			:param ratio: Range: 1E-3 to 1
			:param standard: DMR | DPMR | NXDN | P25 | TETRa | LTE | SPECtrum | CUSTom DMR | DPMR | NXDN | P25 | TETRa | LTE Allows query of the ratio of 'Sample Rate' and 'Max. Sample Rate'. CUSTom Allows set and query of the ratio of 'Sample Rate' and 'Max. Sample Rate'.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('ratio', ratio, DataType.Float), ArgSingle('standard', standard, DataType.Enum, enums.Standard, is_optional=True))
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:RATio {param}'.rstrip())

	def get(self) -> float:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:RATio \n
		Snippet: value: float = driver.configure.vse.measurement.iqRecorder.ratio.get() \n
		Sets or queries the ratio of 'Sample Rate' and 'Max. Sample Rate'. \n
			:return: ratio: Range: 1E-3 to 1"""
		response = self._core.io.query_str(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:RATio?')
		return Conversions.str_to_float(response)
