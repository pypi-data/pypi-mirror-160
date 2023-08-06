from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Minimum:
	"""Minimum commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("minimum", core, parent)

	# noinspection PyTypeChecker
	class CalculateStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Freq_Error: enums.ResultStatus: Carrier frequency error Unit: Hz
			- Power_Rms: enums.ResultStatus: Absolute RMS power of the RF signal Unit: dBm
			- Power_Pep: float or bool: Absolute peak envelope power of the RF signal Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_enum('Freq_Error', enums.ResultStatus),
			ArgStruct.scalar_enum('Power_Rms', enums.ResultStatus),
			ArgStruct.scalar_float_ext('Power_Pep')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Freq_Error: enums.ResultStatus = None
			self.Power_Rms: enums.ResultStatus = None
			self.Power_Pep: float or bool = None

	def calculate(self) -> CalculateStruct:
		"""SCPI: CALCulate:AFRF:MEASurement<Instance>:MEValuation:RFCarrier:MINimum \n
		Snippet: value: CalculateStruct = driver.afRf.measurement.multiEval.rfCarrier.minimum.calculate() \n
		Queries the RF carrier measurement results. CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for CalculateStruct structure arguments."""
		return self._core.io.query_struct(f'CALCulate:AFRF:MEASurement<Instance>:MEValuation:RFCarrier:MINimum?', self.__class__.CalculateStruct())

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Freq_Error: float: Carrier frequency error Unit: Hz
			- Power_Rms: float: Absolute RMS power of the RF signal Unit: dBm
			- Power_Pep: float: Absolute peak envelope power of the RF signal Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Freq_Error'),
			ArgStruct.scalar_float('Power_Rms'),
			ArgStruct.scalar_float('Power_Pep')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Freq_Error: float = None
			self.Power_Rms: float = None
			self.Power_Pep: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:RFCarrier:MINimum \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.rfCarrier.minimum.fetch() \n
		Queries the RF carrier measurement results. CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:RFCarrier:MINimum?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:RFCarrier:MINimum \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.rfCarrier.minimum.read() \n
		Queries the RF carrier measurement results. CALCulate commands return error indicators instead of measurement values. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:MEValuation:RFCarrier:MINimum?', self.__class__.ResultData())
