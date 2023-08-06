from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dtmf:
	"""Dtmf commands group definition. 5 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dtmf", core, parent)

	@property
	def userDefined(self):
		"""userDefined commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_userDefined'):
			from .UserDefined import UserDefined
			self._userDefined = UserDefined(self._core, self._cmd_group)
		return self._userDefined

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import Frequency
			self._frequency = Frequency(self._core, self._cmd_group)
		return self._frequency

	def get_cfgenerator(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:CFGenerator \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.tones.dtmf.get_cfgenerator() \n
		Couples the DTMF tone settings of the analyzer to the corresponding generator settings. \n
			:return: conf_from_gen: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:CFGenerator?')
		return Conversions.str_to_bool(response)

	def set_cfgenerator(self, conf_from_gen: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:CFGenerator \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dtmf.set_cfgenerator(conf_from_gen = False) \n
		Couples the DTMF tone settings of the analyzer to the corresponding generator settings. \n
			:param conf_from_gen: OFF | ON
		"""
		param = Conversions.bool_to_str(conf_from_gen)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:CFGenerator {param}')

	def get_slength(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:SLENgth \n
		Snippet: value: int = driver.configure.afRf.measurement.multiEval.tones.dtmf.get_slength() \n
		Specifies the expected length of the analyzed DTMF tone sequence (number of digits) . \n
			:return: seq_length: Range: 1 to 42
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, seq_length: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:SLENgth \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dtmf.set_slength(seq_length = 1) \n
		Specifies the expected length of the analyzed DTMF tone sequence (number of digits) . \n
			:param seq_length: Range: 1 to 42
		"""
		param = Conversions.decimal_value_to_str(seq_length)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:SLENgth {param}')

	def clone(self) -> 'Dtmf':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dtmf(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
