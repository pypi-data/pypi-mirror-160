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
			- Power: enums.ResultStatus: Reverse power or forward power Unit: dBm
			- Return_Loss: enums.ResultStatus: Unit: dB
			- Reflection: enums.ResultStatus: Unit: %
			- Swr: enums.ResultStatus: Standing wave ratio"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Power', enums.ResultStatus),
			ArgStruct.scalar_enum('Return_Loss', enums.ResultStatus),
			ArgStruct.scalar_enum('Reflection', enums.ResultStatus),
			ArgStruct.scalar_enum('Swr', enums.ResultStatus)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Power: enums.ResultStatus = None
			self.Return_Loss: enums.ResultStatus = None
			self.Reflection: enums.ResultStatus = None
			self.Swr: enums.ResultStatus = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:GPRF:MEASurement<Instance>:NRT:REVerse:CURRent \n
		Snippet: value: CalculateStruct = driver.gprfMeasurement.nrt.reverse.current.calculate() \n
		Return the measurement results for the reverse direction.
			INTRO_CMD_HELP: The meaning of the result <Power> depends on the value set via the command method RsCma.Configure.GprfMeasurement.Nrt.Forward.Value.enable: \n
			- FPWR or PEP: <Power> is the reverse power.
			- CFAC or CCDF: <Power> is the forward power.
		CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:GPRF:MEASurement<Instance>:NRT:REVerse:CURRent?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Power: float: Reverse power or forward power Unit: dBm
			- Return_Loss: float: Unit: dB
			- Reflection: float: Unit: %
			- Swr: float: Standing wave ratio"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Power'),
			ArgStruct.scalar_float('Return_Loss'),
			ArgStruct.scalar_float('Reflection'),
			ArgStruct.scalar_float('Swr')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Power: float = None
			self.Return_Loss: float = None
			self.Reflection: float = None
			self.Swr: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:NRT:REVerse:CURRent \n
		Snippet: value: ResultData = driver.gprfMeasurement.nrt.reverse.current.fetch() \n
		Return the measurement results for the reverse direction.
			INTRO_CMD_HELP: The meaning of the result <Power> depends on the value set via the command method RsCma.Configure.GprfMeasurement.Nrt.Forward.Value.enable: \n
			- FPWR or PEP: <Power> is the reverse power.
			- CFAC or CCDF: <Power> is the forward power.
		CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:GPRF:MEASurement<Instance>:NRT:REVerse:CURRent?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:GPRF:MEASurement<Instance>:NRT:REVerse:CURRent \n
		Snippet: value: ResultData = driver.gprfMeasurement.nrt.reverse.current.read() \n
		Return the measurement results for the reverse direction.
			INTRO_CMD_HELP: The meaning of the result <Power> depends on the value set via the command method RsCma.Configure.GprfMeasurement.Nrt.Forward.Value.enable: \n
			- FPWR or PEP: <Power> is the reverse power.
			- CFAC or CCDF: <Power> is the forward power.
		CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:GPRF:MEASurement<Instance>:NRT:REVerse:CURRent?', self.__class__.ResultData())
