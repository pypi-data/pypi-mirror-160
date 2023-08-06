from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandwidth:
	"""Bandwidth commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bandwidth", core, parent)

	def set(self, bandpass_bw: float, standard: enums.Standard = None) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth \n
		Snippet: driver.configure.vse.measurement.iqRecorder.filterPy.bandpass.bandwidth.set(bandpass_bw = 1.0, standard = enums.Standard.CUSTom) \n
		Sets or queries the bandwidth of the bandpass filter and the related digital standard. \n
			:param bandpass_bw: Range: 1000 Hz to 160 MHz, Unit: Hz
			:param standard: DMR | DPMR | NXDN | P25 | TETRa | LTE | SPECtrum | CUSTom DMR | DPMR | NXDN | P25 | TETRa | LTE Allows query of the bandwidth of the bandpass filter. CUSTom Allows set and query of the bandwidth of the bandpass filter.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('bandpass_bw', bandpass_bw, DataType.Float), ArgSingle('standard', standard, DataType.Enum, enums.Standard, is_optional=True))
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth {param}'.rstrip())

	def get(self) -> float:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth \n
		Snippet: value: float = driver.configure.vse.measurement.iqRecorder.filterPy.bandpass.bandwidth.get() \n
		Sets or queries the bandwidth of the bandpass filter and the related digital standard. \n
			:return: bandpass_bw: Range: 1000 Hz to 160 MHz, Unit: Hz"""
		response = self._core.io.query_str(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth?')
		return Conversions.str_to_float(response)
