from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Munit:
	"""Munit commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("munit", core, parent)

	def set(self, magnitude_unit: enums.MagnitudeUnit, standard: enums.Standard = None) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:MUNit \n
		Snippet: driver.configure.vse.measurement.iqRecorder.munit.set(magnitude_unit = enums.MagnitudeUnit.RAW, standard = enums.Standard.CUSTom) \n
		Selects or queries the physical unit for representation of the recorded I/Q data. \n
			:param magnitude_unit: VOLT | RAW
			:param standard: DMR | DPMR | NXDN | P25 | TETRa | LTE | SPECtrum | CUSTom DMR | DPMR | NXDN | P25 | TETRa | LTE Allows query of the physical unit. CUSTom Allows set and query of the physical unit.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('magnitude_unit', magnitude_unit, DataType.Enum, enums.MagnitudeUnit), ArgSingle('standard', standard, DataType.Enum, enums.Standard, is_optional=True))
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:MUNit {param}'.rstrip())

	# noinspection PyTypeChecker
	def get(self) -> enums.MagnitudeUnit:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:MUNit \n
		Snippet: value: enums.MagnitudeUnit = driver.configure.vse.measurement.iqRecorder.munit.get() \n
		Selects or queries the physical unit for representation of the recorded I/Q data. \n
			:return: magnitude_unit: VOLT | RAW"""
		response = self._core.io.query_str(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:MUNit?')
		return Conversions.str_to_scalar_enum(response, enums.MagnitudeUnit)
