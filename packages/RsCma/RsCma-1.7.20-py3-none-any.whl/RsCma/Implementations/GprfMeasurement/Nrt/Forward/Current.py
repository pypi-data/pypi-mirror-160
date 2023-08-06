from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Power: enums.ResultStatus: Forward power Unit: dBm
			- Pep: enums.ResultStatus: Unit: dBm
			- Crest_Factor: enums.ResultStatus: Unit: dB
			- Ccdf: enums.ResultStatus: Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Power', enums.ResultStatus),
			ArgStruct.scalar_enum('Pep', enums.ResultStatus),
			ArgStruct.scalar_enum('Crest_Factor', enums.ResultStatus),
			ArgStruct.scalar_enum('Ccdf', enums.ResultStatus)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Power: enums.ResultStatus = None
			self.Pep: enums.ResultStatus = None
			self.Crest_Factor: enums.ResultStatus = None
			self.Ccdf: enums.ResultStatus = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:NRT:FWARd:CURRent \n
		Snippet: value: CalculateStruct = driver.gprfMeasurement.nrt.forward.current.calculate() \n
		Return the measurement results for the forward direction. CALCulate commands return error indicators instead of
		measurement values. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:GPRF:MEASurement<Instance>:NRT:FWARd:CURRent?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Power: float: Forward power Unit: dBm
			- Pep: float: Unit: dBm
			- Crest_Factor: float: Unit: dB
			- Ccdf: float: Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Power'),
			ArgStruct.scalar_float('Pep'),
			ArgStruct.scalar_float('Crest_Factor'),
			ArgStruct.scalar_float('Ccdf')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Power: float = None
			self.Pep: float = None
			self.Crest_Factor: float = None
			self.Ccdf: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:NRT:FWARd:CURRent \n
		Snippet: value: ResultData = driver.gprfMeasurement.nrt.forward.current.fetch() \n
		Return the measurement results for the forward direction. CALCulate commands return error indicators instead of
		measurement values. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:GPRF:MEASurement<Instance>:NRT:FWARd:CURRent?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:GPRF:MEASurement<Instance>:NRT:FWARd:CURRent \n
		Snippet: value: ResultData = driver.gprfMeasurement.nrt.forward.current.read() \n
		Return the measurement results for the forward direction. CALCulate commands return error indicators instead of
		measurement values. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:GPRF:MEASurement<Instance>:NRT:FWARd:CURRent?', self.__class__.ResultData())
