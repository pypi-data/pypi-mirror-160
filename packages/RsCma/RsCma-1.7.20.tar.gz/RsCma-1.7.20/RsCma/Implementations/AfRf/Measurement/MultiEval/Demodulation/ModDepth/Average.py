from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Rms: float: RMS average value Unit: %
			- Rms_Sqrt_2: float: RMS result multiplied with the square root of 2 Unit: %
			- Ppeak: float: Positive peak value Unit: %
			- Mpeak: float: Negative peak value Unit: %
			- Mp_Peak_Average: float: Peak-to-peak value divided by 2 Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Rms'),
			ArgStruct.scalar_float('Rms_Sqrt_2'),
			ArgStruct.scalar_float('Ppeak'),
			ArgStruct.scalar_float('Mpeak'),
			ArgStruct.scalar_float('Mp_Peak_Average')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Rms: float = None
			self.Rms_Sqrt_2: float = None
			self.Ppeak: float = None
			self.Mpeak: float = None
			self.Mp_Peak_Average: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:DEModulation:MDEPth:AVERage \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.demodulation.modDepth.average.fetch() \n
		Query the demodulation results for AM demodulation. A statistical evaluation of the modulation depth is returned. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:DEModulation:MDEPth:AVERage?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:DEModulation:MDEPth:AVERage \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.demodulation.modDepth.average.read() \n
		Query the demodulation results for AM demodulation. A statistical evaluation of the modulation depth is returned. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:MEValuation:DEModulation:MDEPth:AVERage?', self.__class__.ResultData())
