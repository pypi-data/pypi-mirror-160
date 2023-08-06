from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Deviation:
	"""Deviation commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("deviation", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Level_Peak: float: Unit: %
			- Level_Rms: float: Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Level_Peak'),
			ArgStruct.scalar_float('Level_Rms')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Level_Peak: float = None
			self.Level_Rms: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:VOIP:LEVel:DELTa:DEViation \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.voip.level.delta.deviation.fetch() \n
		Query delta results for AF level of VoIP path. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:VOIP:LEVel:DELTa:DEViation?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:VOIP:LEVel:DELTa:DEViation \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.voip.level.delta.deviation.read() \n
		Query delta results for AF level of VoIP path. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:MEValuation:VOIP:LEVel:DELTa:DEViation?', self.__class__.ResultData())
