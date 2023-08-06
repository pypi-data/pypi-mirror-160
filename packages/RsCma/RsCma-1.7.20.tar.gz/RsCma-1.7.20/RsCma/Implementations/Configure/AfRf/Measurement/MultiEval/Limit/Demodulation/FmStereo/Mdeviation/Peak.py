from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal.Types import DataType
from ..........Internal.StructBase import StructBase
from ..........Internal.ArgStruct import ArgStruct
from ..........Internal.ArgSingleList import ArgSingleList
from ..........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Peak:
	"""Peak commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("peak", core, parent)

	def set(self, enable: bool, lower: float = None, upper: float = None) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:PEAK \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.mdeviation.peak.set(enable = False, lower = 1.0, upper = 1.0) \n
		Configures limits for the multiplex deviation results '+Peak' and '-Peak', measured for FM stereo. \n
			:param enable: OFF | ON Enables or disables the limit check
			:param lower: Lower multiplex deviation limit A setting configures also the upper limit (same absolute value, positive sign) . Range: -100 kHz to 0 Hz, Unit: Hz
			:param upper: A query returns the upper multiplex deviation limit. A setting ignores this parameter. Range: 0 Hz to 100 kHz, Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('lower', lower, DataType.Float, None, is_optional=True), ArgSingle('upper', upper, DataType.Float, None, is_optional=True))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:PEAK {param}'.rstrip())

	# noinspection PyTypeChecker
	class PeakStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower multiplex deviation limit A setting configures also the upper limit (same absolute value, positive sign) . Range: -100 kHz to 0 Hz, Unit: Hz
			- Upper: float: A query returns the upper multiplex deviation limit. A setting ignores this parameter. Range: 0 Hz to 100 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> PeakStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:PEAK \n
		Snippet: value: PeakStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.mdeviation.peak.get() \n
		Configures limits for the multiplex deviation results '+Peak' and '-Peak', measured for FM stereo. \n
			:return: structure: for return value, see the help for PeakStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:MDEViation:PEAK?', self.__class__.PeakStruct())
