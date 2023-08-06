from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Binary:
	"""Binary commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("binary", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Symbols_Number: int: Number of values in Symbols.
			- Symbols: List[str]: Comma-separated list of binary values, representing the received bit sequence. The number of values in the list equals the SymbolsNumber."""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Symbols_Number'),
			ArgStruct('Symbols', DataType.RawStringList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Symbols_Number: int = None
			self.Symbols: List[str] = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:VSE:MEASurement<Instance>:NXDN:SYMBols:BINary \n
		Snippet: value: ResultData = driver.vse.measurement.nxdn.symbols.binary.fetch() \n
		Query the received symbols in binary format. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:VSE:MEASurement<Instance>:NXDN:SYMBols:BINary?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:VSE:MEASurement<Instance>:NXDN:SYMBols:BINary \n
		Snippet: value: ResultData = driver.vse.measurement.nxdn.symbols.binary.read() \n
		Query the received symbols in binary format. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:VSE:MEASurement<Instance>:NXDN:SYMBols:BINary?', self.__class__.ResultData())
