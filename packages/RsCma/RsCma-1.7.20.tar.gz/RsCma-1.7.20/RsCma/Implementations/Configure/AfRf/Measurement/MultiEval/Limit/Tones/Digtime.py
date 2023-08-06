from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Digtime:
	"""Digtime commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("digtime", core, parent)

	def set(self, enable: bool, lower: float, upper: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGTime \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.digtime.set(enable = False, lower = 1.0, upper = 1.0) \n
		Configures limits for the digit duration in an analyzed tone sequence (DTMF, free dialing and SelCall) . \n
			:param enable: OFF | ON Enables or disables the limit check
			:param lower: Lower digit-duration limit Range: -100 % to 0 %, Unit: %
			:param upper: Upper digit-duration limit Range: 0 % to 100 %, Unit: %
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('lower', lower, DataType.Float), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGTime {param}'.rstrip())

	# noinspection PyTypeChecker
	class DigtimeStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower digit-duration limit Range: -100 % to 0 %, Unit: %
			- Upper: float: Upper digit-duration limit Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> DigtimeStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGTime \n
		Snippet: value: DigtimeStruct = driver.configure.afRf.measurement.multiEval.limit.tones.digtime.get() \n
		Configures limits for the digit duration in an analyzed tone sequence (DTMF, free dialing and SelCall) . \n
			:return: structure: for return value, see the help for DigtimeStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGTime?', self.__class__.DigtimeStruct())
