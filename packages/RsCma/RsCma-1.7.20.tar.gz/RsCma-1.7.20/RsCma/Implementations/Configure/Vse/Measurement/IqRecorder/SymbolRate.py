from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SymbolRate:
	"""SymbolRate commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("symbolRate", core, parent)

	def set(self, sample_rate: float, standard: enums.Standard = None) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:SRATe \n
		Snippet: driver.configure.vse.measurement.iqRecorder.symbolRate.set(sample_rate = 1.0, standard = enums.Standard.CUSTom) \n
		Sets or queries the sample rate of the IQ recorder. \n
			:param sample_rate: Range: 0 Hz to 200 MHz, Unit: Hz
			:param standard: DMR | DPMR | NXDN | P25 | TETRa | LTE | SPECtrum | CUSTom DMR | DPMR | NXDN | P25 | TETRa | LTE Allows query of the sample rate of the IQ recorder. CUSTom Allows set and query of the sample rate of the IQ recorder.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sample_rate', sample_rate, DataType.Float), ArgSingle('standard', standard, DataType.Enum, enums.Standard, is_optional=True))
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:SRATe {param}'.rstrip())

	def get(self) -> float:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:SRATe \n
		Snippet: value: float = driver.configure.vse.measurement.iqRecorder.symbolRate.get() \n
		Sets or queries the sample rate of the IQ recorder. \n
			:return: sample_rate: Range: 0 Hz to 200 MHz, Unit: Hz"""
		response = self._core.io.query_str(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:SRATe?')
		return Conversions.str_to_float(response)
