from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dtmf:
	"""Dtmf commands group definition. 8 total commands, 2 Subgroups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dtmf", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import Frequency
			self._frequency = Frequency(self._core, self._cmd_group)
		return self._frequency

	@property
	def userDefined(self):
		"""userDefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_userDefined'):
			from .UserDefined import UserDefined
			self._userDefined = UserDefined(self._core, self._cmd_group)
		return self._userDefined

	def get_sequence(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SEQuence \n
		Snippet: value: str = driver.source.afRf.generator.dialing.dtmf.get_sequence() \n
		Specifies a digit sequence for the dialing mode DTMF. \n
			:return: dtm_fsequence: String with 1 to 42 digits The allowed digits are 0 to 9, A to D, * and # (with user-defined tone table also m) .
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SEQuence?')
		return trim_str_response(response)

	def set_sequence(self, dtm_fsequence: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SEQuence \n
		Snippet: driver.source.afRf.generator.dialing.dtmf.set_sequence(dtm_fsequence = '1') \n
		Specifies a digit sequence for the dialing mode DTMF. \n
			:param dtm_fsequence: String with 1 to 42 digits The allowed digits are 0 to 9, A to D, * and # (with user-defined tone table also m) .
		"""
		param = Conversions.value_to_quoted_str(dtm_fsequence)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SEQuence {param}')

	def get_srepeat(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SREPeat \n
		Snippet: value: int = driver.source.afRf.generator.dialing.dtmf.get_srepeat() \n
		Defines how often a DTMF sequence is repeated. \n
			:return: sequence_repeat: Range: 1 to 100
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SREPeat?')
		return Conversions.str_to_int(response)

	def set_srepeat(self, sequence_repeat: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SREPeat \n
		Snippet: driver.source.afRf.generator.dialing.dtmf.set_srepeat(sequence_repeat = 1) \n
		Defines how often a DTMF sequence is repeated. \n
			:param sequence_repeat: Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(sequence_repeat)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SREPeat {param}')

	def get_spause(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SPAuse \n
		Snippet: value: float = driver.source.afRf.generator.dialing.dtmf.get_spause() \n
		Defines the duration of a pause between two repetitions of a DTMF sequence. \n
			:return: sequence_pause: Range: 0 s to 10 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SPAuse?')
		return Conversions.str_to_float(response)

	def set_spause(self, sequence_pause: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SPAuse \n
		Snippet: driver.source.afRf.generator.dialing.dtmf.set_spause(sequence_pause = 1.0) \n
		Defines the duration of a pause between two repetitions of a DTMF sequence. \n
			:param sequence_pause: Range: 0 s to 10 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(sequence_pause)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:SPAuse {param}')

	def get_dtime(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:DTIMe \n
		Snippet: value: float = driver.source.afRf.generator.dialing.dtmf.get_dtime() \n
		Defines the duration of a single digit of a DTMF sequence. \n
			:return: digit_time: Range: 0.02 s to 3 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:DTIMe?')
		return Conversions.str_to_float(response)

	def set_dtime(self, digit_time: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:DTIMe \n
		Snippet: driver.source.afRf.generator.dialing.dtmf.set_dtime(digit_time = 1.0) \n
		Defines the duration of a single digit of a DTMF sequence. \n
			:param digit_time: Range: 0.02 s to 3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(digit_time)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:DTIMe {param}')

	def get_dpause(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:DPAuse \n
		Snippet: value: float = driver.source.afRf.generator.dialing.dtmf.get_dpause() \n
		Defines the duration of the pause between two digits of a DTMF sequence. \n
			:return: digit_pause: Range: 0 s to 3 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:DPAuse?')
		return Conversions.str_to_float(response)

	def set_dpause(self, digit_pause: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:DPAuse \n
		Snippet: driver.source.afRf.generator.dialing.dtmf.set_dpause(digit_pause = 1.0) \n
		Defines the duration of the pause between two digits of a DTMF sequence. \n
			:param digit_pause: Range: 0 s to 3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(digit_pause)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:DPAuse {param}')

	def clone(self) -> 'Dtmf':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dtmf(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
