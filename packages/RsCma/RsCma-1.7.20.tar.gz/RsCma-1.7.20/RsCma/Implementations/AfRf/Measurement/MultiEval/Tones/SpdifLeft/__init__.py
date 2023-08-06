from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpdifLeft:
	"""SpdifLeft commands group definition. 6 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spdifLeft", core, parent)

	@property
	def sequence(self):
		"""sequence commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sequence'):
			from .Sequence import Sequence
			self._sequence = Sequence(self._core, self._cmd_group)
		return self._sequence

	@property
	def repetitions(self):
		"""repetitions commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_repetitions'):
			from .Repetitions import Repetitions
			self._repetitions = Repetitions(self._core, self._cmd_group)
		return self._repetitions

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Length: int: Length of the tone sequence (number of digits)
			- Sequence: List[str]: Dialed digit as string
			- Frequency_1: List[float]: Nominal tone frequency according to the tone table Unit: Hz
			- Deviation_1: List[float]: Deviation of the measured tone frequency from the nominal tone frequency Unit: Hz
			- Fequency_2: List[float]: Second nominal frequency (only relevant for dual tones) Unit: Hz
			- Deviation_2: List[float]: Deviation of the second frequency (only relevant for dual tones) Unit: Hz
			- Time: List[float]: Measured tone duration Unit: s
			- Pause: List[float]: Duration of the pause between this tone and the next tone of the sequence Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Length'),
			ArgStruct('Sequence', DataType.StringList, None, False, True, 1),
			ArgStruct('Frequency_1', DataType.FloatList, None, False, True, 1),
			ArgStruct('Deviation_1', DataType.FloatList, None, False, True, 1),
			ArgStruct('Fequency_2', DataType.FloatList, None, False, True, 1),
			ArgStruct('Deviation_2', DataType.FloatList, None, False, True, 1),
			ArgStruct('Time', DataType.FloatList, None, False, True, 1),
			ArgStruct('Pause', DataType.FloatList, None, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Length: int = None
			self.Sequence: List[str] = None
			self.Frequency_1: List[float] = None
			self.Deviation_1: List[float] = None
			self.Fequency_2: List[float] = None
			self.Deviation_2: List[float] = None
			self.Time: List[float] = None
			self.Pause: List[float] = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:SINLeft \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.tones.spdifLeft.fetch() \n
		Query all results of a tone sequence analysis. For each tone, a sequence of results is returned: <Reliability>, <Length>{,
		<Sequence>, <Frequency1>, <Deviation1>, <Frequency2>, <Deviation2>, <Time>, <Pause>}Tone 1, {...}Tone 2, ..., {...}Tone
		<Length> \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:SINLeft?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:TONes:SINLeft \n
		Snippet: value: ResultData = driver.afRf.measurement.multiEval.tones.spdifLeft.read() \n
		Query all results of a tone sequence analysis. For each tone, a sequence of results is returned: <Reliability>, <Length>{,
		<Sequence>, <Frequency1>, <Deviation1>, <Frequency2>, <Deviation2>, <Time>, <Pause>}Tone 1, {...}Tone 2, ..., {...}Tone
		<Length> \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:MEValuation:TONes:SINLeft?', self.__class__.ResultData())

	def clone(self) -> 'SpdifLeft':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SpdifLeft(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
