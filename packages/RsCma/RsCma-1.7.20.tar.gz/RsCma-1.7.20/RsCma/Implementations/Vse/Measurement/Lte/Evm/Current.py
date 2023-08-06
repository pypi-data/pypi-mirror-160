from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Current:
	"""Current commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("current", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Pusch_Qpsk: float: Unit: %
			- Dmrs_Pusch_Qpsk: float: Unit: %
			- Pucch: float: Unit: %
			- Dmrs_Pucch: float: Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Pusch_Qpsk'),
			ArgStruct.scalar_float('Dmrs_Pusch_Qpsk'),
			ArgStruct.scalar_float('Pucch'),
			ArgStruct.scalar_float('Dmrs_Pucch')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Pusch_Qpsk: float = None
			self.Dmrs_Pusch_Qpsk: float = None
			self.Pucch: float = None
			self.Dmrs_Pucch: float = None

	def read(self) -> ResultData:
		"""SCPI: READ:VSE:MEASurement<Instance>:LTE:EVM:CURRent \n
		Snippet: value: ResultData = driver.vse.measurement.lte.evm.current.read() \n
		Query LTE EVM results. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:VSE:MEASurement<Instance>:LTE:EVM:CURRent?', self.__class__.ResultData())

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:VSE:MEASurement<Instance>:LTE:EVM:CURRent \n
		Snippet: value: ResultData = driver.vse.measurement.lte.evm.current.fetch() \n
		Query LTE EVM results. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:VSE:MEASurement<Instance>:LTE:EVM:CURRent?', self.__class__.ResultData())
