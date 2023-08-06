from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tsensitivity:
	"""Tsensitivity commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tsensitivity", core, parent)

	def set(self, enable: bool, lower: float = None, upper: float = None) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:TSENsitivity \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.rsquelch.tsensitivity.set(enable = False, lower = 1.0, upper = 1.0) \n
		Enables a limit check and sets limits for the squelch off level. \n
			:param enable: OFF | ON
			:param lower: Range: -130 dBm to -106 dBm, Unit: dBm
			:param upper: Range: -108 dBm to -30 dBm, Unit: dBm
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('lower', lower, DataType.Float, None, is_optional=True), ArgSingle('upper', upper, DataType.Float, None, is_optional=True))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:TSENsitivity {param}'.rstrip())

	# noinspection PyTypeChecker
	class TsensitivityStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON
			- Lower: float: Range: -130 dBm to -106 dBm, Unit: dBm
			- Upper: float: Range: -108 dBm to -30 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get(self) -> TsensitivityStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:TSENsitivity \n
		Snippet: value: TsensitivityStruct = driver.configure.afRf.measurement.searchRoutines.limit.rsquelch.tsensitivity.get() \n
		Enables a limit check and sets limits for the squelch off level. \n
			:return: structure: for return value, see the help for TsensitivityStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RSQuelch:TSENsitivity?', self.__class__.TsensitivityStruct())
