from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Thysteresis:
	"""Thysteresis commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("thysteresis", core, parent)

	def set(self, enable: bool, lower: float = None, upper: float = None) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:THYSteresis \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.rsquelch.thysteresis.set(enable = False, lower = 1.0, upper = 1.0) \n
		Enables a limit check and sets limits for the squelch hysteresis result. \n
			:param enable: OFF | ON
			:param lower: Range: 0.1 dB to 3.0 dB, Unit: dB
			:param upper: Range: 1.0 dB to 10 dB, Unit: dB
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('lower', lower, DataType.Float, None, is_optional=True), ArgSingle('upper', upper, DataType.Float, None, is_optional=True))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:THYSteresis {param}'.rstrip())

	# noinspection PyTypeChecker
	class ThysteresisStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON
			- Lower: float: Range: 0.1 dB to 3.0 dB, Unit: dB
			- Upper: float: Range: 1.0 dB to 10 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> ThysteresisStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:THYSteresis \n
		Snippet: value: ThysteresisStruct = driver.configure.afRf.measurement.searchRoutines.limit.rsquelch.thysteresis.get() \n
		Enables a limit check and sets limits for the squelch hysteresis result. \n
			:return: structure: for return value, see the help for ThysteresisStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:THYSteresis?', self.__class__.ThysteresisStruct())
