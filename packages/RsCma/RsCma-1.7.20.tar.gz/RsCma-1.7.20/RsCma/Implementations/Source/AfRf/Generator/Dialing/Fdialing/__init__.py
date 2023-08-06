from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fdialing:
	"""Fdialing commands group definition. 8 total commands, 1 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fdialing", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import Frequency
			self._frequency = Frequency(self._core, self._cmd_group)
		return self._frequency

	# noinspection PyTypeChecker
	def get_ttype(self) -> enums.SingDualTonesType:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:TTYPe \n
		Snippet: value: enums.SingDualTonesType = driver.source.afRf.generator.dialing.fdialing.get_ttype() \n
		Selects the tone type for free dialing. \n
			:return: tone_type: STONes | DTONes Single tones or dual tones
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:TTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.SingDualTonesType)

	def set_ttype(self, tone_type: enums.SingDualTonesType) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:TTYPe \n
		Snippet: driver.source.afRf.generator.dialing.fdialing.set_ttype(tone_type = enums.SingDualTonesType.DTONes) \n
		Selects the tone type for free dialing. \n
			:param tone_type: STONes | DTONes Single tones or dual tones
		"""
		param = Conversions.enum_scalar_to_str(tone_type, enums.SingDualTonesType)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:TTYPe {param}')

	def get_sequence(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SEQuence \n
		Snippet: value: str = driver.source.afRf.generator.dialing.fdialing.get_sequence() \n
		Specifies a digit sequence for the mode free dialing. \n
			:return: fdialing_sequence: String with 1 to 42 digits The allowed digits are 0 to 9, A to F and m.
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SEQuence?')
		return trim_str_response(response)

	def set_sequence(self, fdialing_sequence: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SEQuence \n
		Snippet: driver.source.afRf.generator.dialing.fdialing.set_sequence(fdialing_sequence = '1') \n
		Specifies a digit sequence for the mode free dialing. \n
			:param fdialing_sequence: String with 1 to 42 digits The allowed digits are 0 to 9, A to F and m.
		"""
		param = Conversions.value_to_quoted_str(fdialing_sequence)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SEQuence {param}')

	def get_srepeat(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SREPeat \n
		Snippet: value: int = driver.source.afRf.generator.dialing.fdialing.get_srepeat() \n
		Defines how often a free-dialing sequence is repeated. \n
			:return: sequence_repeat: Range: 1 to 100
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SREPeat?')
		return Conversions.str_to_int(response)

	def set_srepeat(self, sequence_repeat: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SREPeat \n
		Snippet: driver.source.afRf.generator.dialing.fdialing.set_srepeat(sequence_repeat = 1) \n
		Defines how often a free-dialing sequence is repeated. \n
			:param sequence_repeat: Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(sequence_repeat)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SREPeat {param}')

	def get_spause(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SPAuse \n
		Snippet: value: float = driver.source.afRf.generator.dialing.fdialing.get_spause() \n
		Defines the duration of a pause between two repetitions of a free-dialing sequence. \n
			:return: sequence_pause: Range: 0 s to 10 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SPAuse?')
		return Conversions.str_to_float(response)

	def set_spause(self, sequence_pause: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SPAuse \n
		Snippet: driver.source.afRf.generator.dialing.fdialing.set_spause(sequence_pause = 1.0) \n
		Defines the duration of a pause between two repetitions of a free-dialing sequence. \n
			:param sequence_pause: Range: 0 s to 10 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(sequence_pause)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:SPAuse {param}')

	def get_dtime(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:DTIMe \n
		Snippet: value: float = driver.source.afRf.generator.dialing.fdialing.get_dtime() \n
		Defines the duration of a single digit of a free-dialing sequence. \n
			:return: digit_time: Range: 0.02 s to 3 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:DTIMe?')
		return Conversions.str_to_float(response)

	def set_dtime(self, digit_time: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:DTIMe \n
		Snippet: driver.source.afRf.generator.dialing.fdialing.set_dtime(digit_time = 1.0) \n
		Defines the duration of a single digit of a free-dialing sequence. \n
			:param digit_time: Range: 0.02 s to 3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(digit_time)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:DTIMe {param}')

	def get_dpause(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:DPAuse \n
		Snippet: value: float = driver.source.afRf.generator.dialing.fdialing.get_dpause() \n
		Defines the duration of the pause between two digits of a free-dialing sequence. \n
			:return: digit_pause: Range: 0 s to 3 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:DPAuse?')
		return Conversions.str_to_float(response)

	def set_dpause(self, digit_pause: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:DPAuse \n
		Snippet: driver.source.afRf.generator.dialing.fdialing.set_dpause(digit_pause = 1.0) \n
		Defines the duration of the pause between two digits of a free-dialing sequence. \n
			:param digit_pause: Range: 0 s to 3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(digit_pause)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:FDIaling:DPAuse {param}')

	def clone(self) -> 'Fdialing':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fdialing(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
