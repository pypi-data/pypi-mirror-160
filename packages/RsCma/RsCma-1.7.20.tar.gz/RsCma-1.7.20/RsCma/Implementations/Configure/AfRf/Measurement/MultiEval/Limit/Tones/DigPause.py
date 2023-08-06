from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DigPause:
	"""DigPause commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("digPause", core, parent)

	def set(self, enable: bool, lower: float, upper: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGPause \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.digPause.set(enable = False, lower = 1.0, upper = 1.0) \n
		Configures limits for the pause between two tones of an analyzed tone sequence (DTMF, free dialing and SelCall) . \n
			:param enable: OFF | ON Enables or disables the limit check
			:param lower: Lower pause limit Range: -100 % to 0 %, Unit: %
			:param upper: Upper pause limit Range: 0 % to 100 %, Unit: %
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('lower', lower, DataType.Float), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGPause {param}'.rstrip())

	# noinspection PyTypeChecker
	class DigPauseStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower pause limit Range: -100 % to 0 %, Unit: %
			- Upper: float: Upper pause limit Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> DigPauseStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGPause \n
		Snippet: value: DigPauseStruct = driver.configure.afRf.measurement.multiEval.limit.tones.digPause.get() \n
		Configures limits for the pause between two tones of an analyzed tone sequence (DTMF, free dialing and SelCall) . \n
			:return: structure: for return value, see the help for DigPauseStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGPause?', self.__class__.DigPauseStruct())
