from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Maximum:
	"""Maximum commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("maximum", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Freq_Error: float: Unit: Hz
			- Power_Pep: float: Unit: dBm
			- Freq_Drift: List[float]: Unit: Hz/symbol"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Freq_Error'),
			ArgStruct.scalar_float('Power_Pep'),
			ArgStruct('Freq_Drift', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Freq_Error: float = None
			self.Power_Pep: float = None
			self.Freq_Drift: List[float] = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:VSE:MEASurement<Instance>:RFCarrier:MAXimum \n
		Snippet: value: ResultData = driver.vse.measurement.rfCarrier.maximum.fetch() \n
		Query the RF results. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:VSE:MEASurement<Instance>:RFCarrier:MAXimum?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:VSE:MEASurement<Instance>:RFCarrier:MAXimum \n
		Snippet: value: ResultData = driver.vse.measurement.rfCarrier.maximum.read() \n
		Query the RF results. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:VSE:MEASurement<Instance>:RFCarrier:MAXimum?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Freq_Error: enums.ResultStatus: Unit: Hz
			- Power_Pep: enums.ResultStatus: Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Freq_Error', enums.ResultStatus),
			ArgStruct.scalar_enum('Power_Pep', enums.ResultStatus)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Freq_Error: enums.ResultStatus = None
			self.Power_Pep: enums.ResultStatus = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:VSE:MEASurement<Instance>:RFCarrier:MAXimum \n
		Snippet: value: CalculateStruct = driver.vse.measurement.rfCarrier.maximum.calculate() \n
		Query the RF results. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:VSE:MEASurement<Instance>:RFCarrier:MAXimum?', self.__class__.CalculateStruct())
