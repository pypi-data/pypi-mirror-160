from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dcs:
	"""Dcs commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dcs", core, parent)

	@property
	def timeout(self):
		"""timeout commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_timeout'):
			from .Timeout import Timeout
			self._timeout = Timeout(self._core, self._cmd_group)
		return self._timeout

	def get_ec_word(self) -> str:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:ECWord \n
		Snippet: value: str = driver.configure.afRf.measurement.multiEval.tones.dcs.get_ec_word() \n
		Specifies the expected DCS code number. \n
			:return: exp_code_word: DCS code number as octal number Not allowed octal numbers are automatically rounded to the closest allowed value, see method RsCma.Source.AfRf.Generator.Tones.Dcs.cword. Range: #Q20 to #Q777
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:ECWord?')
		return trim_str_response(response)

	def set_ec_word(self, exp_code_word: str) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:ECWord \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dcs.set_ec_word(exp_code_word = r1) \n
		Specifies the expected DCS code number. \n
			:param exp_code_word: DCS code number as octal number Not allowed octal numbers are automatically rounded to the closest allowed value, see method RsCma.Source.AfRf.Generator.Tones.Dcs.cword. Range: #Q20 to #Q777
		"""
		param = Conversions.value_to_str(exp_code_word)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:ECWord {param}')

	def get_imodulation(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:IMODulation \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.tones.dcs.get_imodulation() \n
		Enables or disables the inversion of the FSK demodulation polarity. \n
			:return: imodulation: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:IMODulation?')
		return Conversions.str_to_bool(response)

	def set_imodulation(self, imodulation: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:IMODulation \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dcs.set_imodulation(imodulation = False) \n
		Enables or disables the inversion of the FSK demodulation polarity. \n
			:param imodulation: OFF | ON
		"""
		param = Conversions.bool_to_str(imodulation)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:IMODulation {param}')

	def clone(self) -> 'Dcs':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dcs(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
