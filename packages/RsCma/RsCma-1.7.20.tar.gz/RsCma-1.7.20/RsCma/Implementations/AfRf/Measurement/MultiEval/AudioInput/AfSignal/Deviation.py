from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import repcap


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
			- Frequency: float: Frequency of the measured AF signal Unit: Hz
			- Level: float: Effective level of the AC component of the measured AF signal Unit: V
			- Dc_Level: float: Level of the DC component of the measured AF signal (input coupling DC required) Unit: V"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Frequency'),
			ArgStruct.scalar_float('Level'),
			ArgStruct.scalar_float('Dc_Level')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Frequency: float = None
			self.Level: float = None
			self.Dc_Level: float = None

	def fetch(self, audioInput=repcap.AudioInput.Default) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:AIN<Nr>:AFSignal:DEViation \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.audioInput.afSignal.deviation.fetch(audioInput = repcap.AudioInput.Default) \n
		Query the AF frequency and level results measured for an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:AIN{audioInput_cmd_val}:AFSignal:DEViation?', self.__class__.ResultData())

	def read(self, audioInput=repcap.AudioInput.Default) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:AIN<Nr>:AFSignal:DEViation \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.audioInput.afSignal.deviation.read(audioInput = repcap.AudioInput.Default) \n
		Query the AF frequency and level results measured for an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: structure: for return value, see the help for ResultData structure arguments."""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:MEValuation:AIN{audioInput_cmd_val}:AFSignal:DEViation?', self.__class__.ResultData())
