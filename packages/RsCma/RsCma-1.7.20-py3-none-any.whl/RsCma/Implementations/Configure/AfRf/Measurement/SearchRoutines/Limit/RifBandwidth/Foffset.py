from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Foffset:
	"""Foffset commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("foffset", core, parent)

	def set(self, enable: bool, upper: float = None) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:FOFFset \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.rifBandwidth.foffset.set(enable = False, upper = 1.0) \n
		Set the upper limit for the center frequency offset. \n
			:param enable: OFF | ON
			:param upper: Range: 1 Hz to 50000 Hz, Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('upper', upper, DataType.Float, None, is_optional=True))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:FOFFset {param}'.rstrip())

	# noinspection PyTypeChecker
	class FoffsetStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON
			- Upper: float: Range: 1 Hz to 50000 Hz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get(self) -> FoffsetStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:FOFFset \n
		Snippet: value: FoffsetStruct = driver.configure.afRf.measurement.searchRoutines.limit.rifBandwidth.foffset.get() \n
		Set the upper limit for the center frequency offset. \n
			:return: structure: for return value, see the help for FoffsetStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:RIFBandwidth:FOFFset?', self.__class__.FoffsetStruct())
