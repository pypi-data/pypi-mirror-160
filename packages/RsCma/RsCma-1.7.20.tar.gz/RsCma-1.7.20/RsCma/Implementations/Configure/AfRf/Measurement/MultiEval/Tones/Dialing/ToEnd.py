from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ToEnd:
	"""ToEnd commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("toEnd", core, parent)

	def set(self, enable: bool, timeout: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOENd \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dialing.toEnd.set(enable = False, timeout = 1.0) \n
		Configures a timeout for waiting for the next tone during a dialing sequence analysis. \n
			:param enable: OFF | ON Enables the timeout
			:param timeout: Maximum time interval after the end of a tone and the start of the next tone Range: 0.1 s to 30 s, Unit: s
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('timeout', timeout, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOENd {param}'.rstrip())

	# noinspection PyTypeChecker
	class ToEndStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables the timeout
			- Timeout: float: Maximum time interval after the end of a tone and the start of the next tone Range: 0.1 s to 30 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Timeout')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Timeout: float = None

	def get(self) -> ToEndStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOENd \n
		Snippet: value: ToEndStruct = driver.configure.afRf.measurement.multiEval.tones.dialing.toEnd.get() \n
		Configures a timeout for waiting for the next tone during a dialing sequence analysis. \n
			:return: structure: for return value, see the help for ToEndStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DIALing:TOENd?', self.__class__.ToEndStruct())
