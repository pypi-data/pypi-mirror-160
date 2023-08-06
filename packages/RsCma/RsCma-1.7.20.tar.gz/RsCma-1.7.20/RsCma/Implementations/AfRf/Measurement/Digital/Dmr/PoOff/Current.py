from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


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
			- Power_Slot_0: float: Unit: dBm
			- Power_Slot_1: float: Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Power_Slot_0'),
			ArgStruct.scalar_float('Power_Slot_1')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Power_Slot_0: float = None
			self.Power_Slot_1: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:DIGital:DMR:POOFf:CURRent \n
		Snippet: value: ResultData = driver.afRf.measurement.digital.dmr.poOff.current.fetch() \n
		For DMR, query the current power level on the on-time slot (i.e.'Power On (Slot 0) ') and the current power level on the
		off-time slot (i.e. 'Power OFF (Slot 1) '. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:DIGital:DMR:POOFf:CURRent?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:DIGital:DMR:POOFf:CURRent \n
		Snippet: value: ResultData = driver.afRf.measurement.digital.dmr.poOff.current.read() \n
		For DMR, query the current power level on the on-time slot (i.e.'Power On (Slot 0) ') and the current power level on the
		off-time slot (i.e. 'Power OFF (Slot 1) '. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:DIGital:DMR:POOFf:CURRent?', self.__class__.ResultData())
