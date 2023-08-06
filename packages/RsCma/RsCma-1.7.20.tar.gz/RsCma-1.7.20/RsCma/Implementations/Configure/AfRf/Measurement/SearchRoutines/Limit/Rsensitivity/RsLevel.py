from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RsLevel:
	"""RsLevel commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rsLevel", core, parent)

	def set(self, enable: bool, upper: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSENsitivity:RSLevel \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.rsensitivity.rsLevel.set(enable = False, upper = 1.0) \n
		Configures an upper limit for the measured RX sensitivity. \n
			:param enable: OFF | ON Enables or disables the limit check
			:param upper: Upper limit for the RX sensitivity Range: -120 dBm to -100 dBm, Unit: dBm
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSENsitivity:RSLevel {param}'.rstrip())

	# noinspection PyTypeChecker
	class RsLevelStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper limit for the RX sensitivity Range: -120 dBm to -100 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get(self) -> RsLevelStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSENsitivity:RSLevel \n
		Snippet: value: RsLevelStruct = driver.configure.afRf.measurement.searchRoutines.limit.rsensitivity.rsLevel.get() \n
		Configures an upper limit for the measured RX sensitivity. \n
			:return: structure: for return value, see the help for RsLevelStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSENsitivity:RSLevel?', self.__class__.RsLevelStruct())
