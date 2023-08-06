from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SelCall:
	"""SelCall commands group definition. 7 total commands, 2 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("selCall", core, parent)

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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:CFGenerator \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.tones.selCall.get_cfgenerator() \n
		Couples the SelCall tone settings of the analyzer to the corresponding generator settings. \n
			:return: conf_from_gen: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:CFGenerator?')
		return Conversions.str_to_bool(response)

	def set_cfgenerator(self, conf_from_gen: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:CFGenerator \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.selCall.set_cfgenerator(conf_from_gen = False) \n
		Couples the SelCall tone settings of the analyzer to the corresponding generator settings. \n
			:param conf_from_gen: OFF | ON
		"""
		param = Conversions.bool_to_str(conf_from_gen)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:CFGenerator {param}')

	def get_slength(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:SLENgth \n
		Snippet: value: int = driver.configure.afRf.measurement.multiEval.tones.selCall.get_slength() \n
		Specifies the expected length of the analyzed SelCall tone sequence (number of digits) . By default, the user-defined
		tone definition is disabled, and the length is fixed (five digits) . If the user-defined tone definition is enabled, you
		can configure the length. \n
			:return: seq_length: Range: 2 to 42
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, seq_length: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:SLENgth \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.selCall.set_slength(seq_length = 1) \n
		Specifies the expected length of the analyzed SelCall tone sequence (number of digits) . By default, the user-defined
		tone definition is disabled, and the length is fixed (five digits) . If the user-defined tone definition is enabled, you
		can configure the length. \n
			:param seq_length: Range: 2 to 42
		"""
		param = Conversions.decimal_value_to_str(seq_length)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_standard(self) -> enums.SelCallStandard:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:STANdard \n
		Snippet: value: enums.SelCallStandard = driver.configure.afRf.measurement.multiEval.tones.selCall.get_standard() \n
		Selects a selective-calling standard for SelCall tone sequence analysis. \n
			:return: sel_call_standard: CCIR | EEA | EIA | ZVEI1 | ZVEI2 | ZVEI3 | DZVei | PZVei
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.SelCallStandard)

	def set_standard(self, sel_call_standard: enums.SelCallStandard) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:STANdard \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.selCall.set_standard(sel_call_standard = enums.SelCallStandard.CCIR) \n
		Selects a selective-calling standard for SelCall tone sequence analysis. \n
			:param sel_call_standard: CCIR | EEA | EIA | ZVEI1 | ZVEI2 | ZVEI3 | DZVei | PZVei
		"""
		param = Conversions.enum_scalar_to_str(sel_call_standard, enums.SelCallStandard)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:STANdard {param}')

	# noinspection PyTypeChecker
	def get_maccuracy(self) -> enums.MeasAccuracy:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:MACCuracy \n
		Snippet: value: enums.MeasAccuracy = driver.configure.afRf.measurement.multiEval.tones.selCall.get_maccuracy() \n
		Configures the accuracy of the analysis of SelCall tone sequences. \n
			:return: meas_accuracy: NORMal | HIGH NORMal: lower tone detection accuracy / minimum pause length HIGH: higher tone detection accuracy / minimum pause length
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:MACCuracy?')
		return Conversions.str_to_scalar_enum(response, enums.MeasAccuracy)

	def set_maccuracy(self, meas_accuracy: enums.MeasAccuracy) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:MACCuracy \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.selCall.set_maccuracy(meas_accuracy = enums.MeasAccuracy.HIGH) \n
		Configures the accuracy of the analysis of SelCall tone sequences. \n
			:param meas_accuracy: NORMal | HIGH NORMal: lower tone detection accuracy / minimum pause length HIGH: higher tone detection accuracy / minimum pause length
		"""
		param = Conversions.enum_scalar_to_str(meas_accuracy, enums.MeasAccuracy)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:MACCuracy {param}')

	def clone(self) -> 'SelCall':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SelCall(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
