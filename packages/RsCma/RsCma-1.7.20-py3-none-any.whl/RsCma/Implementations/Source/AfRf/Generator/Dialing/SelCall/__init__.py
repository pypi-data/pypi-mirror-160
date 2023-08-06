from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelCall:
	"""SelCall commands group definition. 10 total commands, 2 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("selCall", core, parent)

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

	# noinspection PyTypeChecker
	def get_standard(self) -> enums.SelCallStandard:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:STANdard \n
		Snippet: value: enums.SelCallStandard = driver.source.afRf.generator.dialing.selCall.get_standard() \n
		Selects the SelCall standard and thus the tone definition. \n
			:return: sel_call_standard: CCIR | EEA | EIA | ZVEI1 | ZVEI2 | ZVEI3 | DZVei | PZVei
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.SelCallStandard)

	def set_standard(self, sel_call_standard: enums.SelCallStandard) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:STANdard \n
		Snippet: driver.source.afRf.generator.dialing.selCall.set_standard(sel_call_standard = enums.SelCallStandard.CCIR) \n
		Selects the SelCall standard and thus the tone definition. \n
			:param sel_call_standard: CCIR | EEA | EIA | ZVEI1 | ZVEI2 | ZVEI3 | DZVei | PZVei
		"""
		param = Conversions.enum_scalar_to_str(sel_call_standard, enums.SelCallStandard)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:STANdard {param}')

	def get_sequence(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SEQuence \n
		Snippet: value: str = driver.source.afRf.generator.dialing.selCall.get_sequence() \n
		Specifies a digit sequence for the dialing mode SelCall. \n
			:return: sel_call_sequence: String with five digits - allowed digits are 0 to 9 and A to F If the user-defined tone definition is enabled, you can define 1 to 42 digits and also use the digit m.
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SEQuence?')
		return trim_str_response(response)

	def set_sequence(self, sel_call_sequence: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SEQuence \n
		Snippet: driver.source.afRf.generator.dialing.selCall.set_sequence(sel_call_sequence = '1') \n
		Specifies a digit sequence for the dialing mode SelCall. \n
			:param sel_call_sequence: String with five digits - allowed digits are 0 to 9 and A to F If the user-defined tone definition is enabled, you can define 1 to 42 digits and also use the digit m.
		"""
		param = Conversions.value_to_quoted_str(sel_call_sequence)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SEQuence {param}')

	def get_srepeat(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SREPeat \n
		Snippet: value: int = driver.source.afRf.generator.dialing.selCall.get_srepeat() \n
		Defines how often a SelCall sequence is repeated. \n
			:return: sequence_repeat: Range: 1 to 100
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SREPeat?')
		return Conversions.str_to_int(response)

	def set_srepeat(self, sequence_repeat: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SREPeat \n
		Snippet: driver.source.afRf.generator.dialing.selCall.set_srepeat(sequence_repeat = 1) \n
		Defines how often a SelCall sequence is repeated. \n
			:param sequence_repeat: Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(sequence_repeat)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SREPeat {param}')

	def get_spause(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SPAuse \n
		Snippet: value: float = driver.source.afRf.generator.dialing.selCall.get_spause() \n
		Defines the duration of a pause between two repetitions of a SelCall sequence. \n
			:return: sequence_pause: Range: 0 s to 10 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SPAuse?')
		return Conversions.str_to_float(response)

	def set_spause(self, sequence_pause: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SPAuse \n
		Snippet: driver.source.afRf.generator.dialing.selCall.set_spause(sequence_pause = 1.0) \n
		Defines the duration of a pause between two repetitions of a SelCall sequence. \n
			:param sequence_pause: Range: 0 s to 10 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(sequence_pause)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:SPAuse {param}')

	def get_dtime(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DTIMe \n
		Snippet: value: float = driver.source.afRf.generator.dialing.selCall.get_dtime() \n
		Defines the duration of a single digit of a SelCall sequence. \n
			:return: digit_time: Range: 0.02 s to 3 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DTIMe?')
		return Conversions.str_to_float(response)

	def set_dtime(self, digit_time: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DTIMe \n
		Snippet: driver.source.afRf.generator.dialing.selCall.set_dtime(digit_time = 1.0) \n
		Defines the duration of a single digit of a SelCall sequence. \n
			:param digit_time: Range: 0.02 s to 3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(digit_time)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DTIMe {param}')

	def get_dpause(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DPAuse \n
		Snippet: value: float = driver.source.afRf.generator.dialing.selCall.get_dpause() \n
		Defines the duration of the pause between two digits of a SelCall sequence. \n
			:return: digit_pause: Range: 0 s to 3 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DPAuse?')
		return Conversions.str_to_float(response)

	def set_dpause(self, digit_pause: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DPAuse \n
		Snippet: driver.source.afRf.generator.dialing.selCall.set_dpause(digit_pause = 1.0) \n
		Defines the duration of the pause between two digits of a SelCall sequence. \n
			:param digit_pause: Range: 0 s to 3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(digit_pause)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DPAuse {param}')

	def get_drepeat(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DREPeat \n
		Snippet: value: bool = driver.source.afRf.generator.dialing.selCall.get_drepeat() \n
		Enables or disables the usage of the repeat digit for the tone mode SelCall. \n
			:return: digit_repeat: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DREPeat?')
		return Conversions.str_to_bool(response)

	def set_drepeat(self, digit_repeat: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DREPeat \n
		Snippet: driver.source.afRf.generator.dialing.selCall.set_drepeat(digit_repeat = False) \n
		Enables or disables the usage of the repeat digit for the tone mode SelCall. \n
			:param digit_repeat: OFF | ON
		"""
		param = Conversions.bool_to_str(digit_repeat)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:SELCall:DREPeat {param}')

	def clone(self) -> 'SelCall':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SelCall(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
