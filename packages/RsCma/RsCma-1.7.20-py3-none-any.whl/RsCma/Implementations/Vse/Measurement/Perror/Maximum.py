from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
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
			- Reliability: int: No parameter help available
			- Rms: float: Range: -999 deg to 999 deg, Unit: deg
			- Peak: float: Range: -999 deg to 999 deg, Unit: deg"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Rms'),
			ArgStruct.scalar_float('Peak')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Rms: float = None
			self.Peak: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:VSE:MEASurement<Instance>:PERRor:MAXimum \n
		Snippet: value: ResultData = driver.vse.measurement.perror.maximum.fetch() \n
		Query the phase error results. CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:VSE:MEASurement<Instance>:PERRor:MAXimum?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:VSE:MEASurement<Instance>:PERRor:MAXimum \n
		Snippet: value: ResultData = driver.vse.measurement.perror.maximum.read() \n
		Query the phase error results. CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:VSE:MEASurement<Instance>:PERRor:MAXimum?', self.__class__.ResultData())

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Rms: enums.ResultStatus: Range: -999 deg to 999 deg, Unit: deg
			- Peak: enums.ResultStatus: Range: -999 deg to 999 deg, Unit: deg"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Rms', enums.ResultStatus),
			ArgStruct.scalar_enum('Peak', enums.ResultStatus)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Rms: enums.ResultStatus = None
			self.Peak: enums.ResultStatus = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:VSE:MEASurement<Instance>:PERRor:MAXimum \n
		Snippet: value: CalculateStruct = driver.vse.measurement.perror.maximum.calculate() \n
		Query the phase error results. CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:VSE:MEASurement<Instance>:PERRor:MAXimum?', self.__class__.CalculateStruct())
