from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class FetchStruct(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: No parameter help available
			- Delay_Left: float: Unit: s
			- Delay_Right: float: Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Delay_Left'),
			ArgStruct.scalar_float('Delay_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Delay_Left: float = None
			self.Delay_Right: float = None

	def fetch(self) -> FetchStruct:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SIN:DELay:CURRent \n
		Snippet: value: FetchStruct = driver.afRf.measurement.spdif.delay.current.fetch() \n
		Queries the current scalar results for SPDIF left and right audio delay. \n
			:return: structure: for return value, see the help for FetchStruct structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:SIN:DELay:CURRent?', self.__class__.FetchStruct())
