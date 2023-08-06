from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tpause:
	"""Tpause commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tpause", core, parent)

	def set(self, enable: bool, lower: float, upper: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TPAuse \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.scal.tpause.set(enable = False, lower = 1.0, upper = 1.0) \n
		Configures limits for the pause between two dual tones of an analyzed SELCAL sequence. \n
			:param enable: OFF | ON Enables or disables the limit check
			:param lower: Lower pause limit Range: 0.1 s to 0.25 s, Unit: s
			:param upper: Upper pause limit Range: 0.25 s to 3 s, Unit: s
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('lower', lower, DataType.Float), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TPAuse {param}'.rstrip())

	# noinspection PyTypeChecker
	class TpauseStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower pause limit Range: 0.1 s to 0.25 s, Unit: s
			- Upper: float: Upper pause limit Range: 0.25 s to 3 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> TpauseStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TPAuse \n
		Snippet: value: TpauseStruct = driver.configure.afRf.measurement.multiEval.limit.tones.scal.tpause.get() \n
		Configures limits for the pause between two dual tones of an analyzed SELCAL sequence. \n
			:return: structure: for return value, see the help for TpauseStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:SCAL:TPAuse?', self.__class__.TpauseStruct())
