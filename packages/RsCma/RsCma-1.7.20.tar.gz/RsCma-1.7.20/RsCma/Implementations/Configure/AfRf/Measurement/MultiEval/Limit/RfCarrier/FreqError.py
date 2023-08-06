from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FreqError:
	"""FreqError commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("freqError", core, parent)

	def set(self, enable_limit: bool, lower: float = None, upper: float = None) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:FERRor \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.rfCarrier.freqError.set(enable_limit = False, lower = 1.0, upper = 1.0) \n
		Configures limits for the measured RF carrier frequency error. The upper and lower limits have the same absolute value
		but different signs. \n
			:param enable_limit: OFF | ON Enables or disables the limit check
			:param lower: A query returns the lower limit. A setting applies the absolute value to the upper limit and the absolute value plus a negative sign to the lower limit. Range: -50 kHz to 0 Hz, Unit: Hz
			:param upper: A query returns the upper limit. A setting ignores this parameter. Range: 0 Hz to 50 kHz, Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable_limit', enable_limit, DataType.Boolean), ArgSingle('lower', lower, DataType.Float, None, is_optional=True), ArgSingle('upper', upper, DataType.Float, None, is_optional=True))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:FERRor {param}'.rstrip())

	# noinspection PyTypeChecker
	class FreqErrorStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable_Limit: bool: OFF | ON Enables or disables the limit check
			- Lower: float: A query returns the lower limit. A setting applies the absolute value to the upper limit and the absolute value plus a negative sign to the lower limit. Range: -50 kHz to 0 Hz, Unit: Hz
			- Upper: float: A query returns the upper limit. A setting ignores this parameter. Range: 0 Hz to 50 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Limit'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Limit: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> FreqErrorStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:FERRor \n
		Snippet: value: FreqErrorStruct = driver.configure.afRf.measurement.multiEval.limit.rfCarrier.freqError.get() \n
		Configures limits for the measured RF carrier frequency error. The upper and lower limits have the same absolute value
		but different signs. \n
			:return: structure: for return value, see the help for FreqErrorStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:RFCarrier:FERRor?', self.__class__.FreqErrorStruct())
