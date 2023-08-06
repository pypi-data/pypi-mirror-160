from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fdialing:
	"""Fdialing commands group definition. 7 total commands, 1 Subgroups, 5 group commands"""

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

	def get_cfgenerator(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:CFGenerator \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.tones.fdialing.get_cfgenerator() \n
		Couples the free-dialing tone settings of the analyzer to the corresponding generator settings. \n
			:return: conf_from_gen: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:CFGenerator?')
		return Conversions.str_to_bool(response)

	def set_cfgenerator(self, conf_from_gen: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:CFGenerator \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.fdialing.set_cfgenerator(conf_from_gen = False) \n
		Couples the free-dialing tone settings of the analyzer to the corresponding generator settings. \n
			:param conf_from_gen: OFF | ON
		"""
		param = Conversions.bool_to_str(conf_from_gen)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:CFGenerator {param}')

	# noinspection PyTypeChecker
	def get_efrequency(self) -> enums.ExpFrequency:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:EFRequency \n
		Snippet: value: enums.ExpFrequency = driver.configure.afRf.measurement.multiEval.tones.fdialing.get_efrequency() \n
		No command help available \n
			:return: exp_frequency: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:EFRequency?')
		return Conversions.str_to_scalar_enum(response, enums.ExpFrequency)

	def set_efrequency(self, exp_frequency: enums.ExpFrequency) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:EFRequency \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.fdialing.set_efrequency(exp_frequency = enums.ExpFrequency.CONF) \n
		No command help available \n
			:param exp_frequency: No help available
		"""
		param = Conversions.enum_scalar_to_str(exp_frequency, enums.ExpFrequency)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:EFRequency {param}')

	# noinspection PyTypeChecker
	def get_ttype(self) -> enums.SingDualToneType:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:TTYPe \n
		Snippet: value: enums.SingDualToneType = driver.configure.afRf.measurement.multiEval.tones.fdialing.get_ttype() \n
		Selects a tone type for free-dialing tone sequence analysis. \n
			:return: tone_type: STONe | DTONe Single tones or dual tones
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:TTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.SingDualToneType)

	def set_ttype(self, tone_type: enums.SingDualToneType) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:TTYPe \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.fdialing.set_ttype(tone_type = enums.SingDualToneType.DTONe) \n
		Selects a tone type for free-dialing tone sequence analysis. \n
			:param tone_type: STONe | DTONe Single tones or dual tones
		"""
		param = Conversions.enum_scalar_to_str(tone_type, enums.SingDualToneType)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:TTYPe {param}')

	def get_slength(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:SLENgth \n
		Snippet: value: int = driver.configure.afRf.measurement.multiEval.tones.fdialing.get_slength() \n
		Specifies the expected length of the analyzed free-dialing tone sequence (number of digits) . \n
			:return: seq_length: Range: 1 to 42
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, seq_length: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:SLENgth \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.fdialing.set_slength(seq_length = 1) \n
		Specifies the expected length of the analyzed free-dialing tone sequence (number of digits) . \n
			:param seq_length: Range: 1 to 42
		"""
		param = Conversions.decimal_value_to_str(seq_length)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_maccuracy(self) -> enums.MeasAccuracy:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:MACCuracy \n
		Snippet: value: enums.MeasAccuracy = driver.configure.afRf.measurement.multiEval.tones.fdialing.get_maccuracy() \n
		Configures the accuracy of the analysis of free-dialing single-tone sequences. \n
			:return: meas_accuracy: NORMal | HIGH NORMal: lower tone detection accuracy / minimum pause length HIGH: higher tone detection accuracy / minimum pause length
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:MACCuracy?')
		return Conversions.str_to_scalar_enum(response, enums.MeasAccuracy)

	def set_maccuracy(self, meas_accuracy: enums.MeasAccuracy) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:MACCuracy \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.fdialing.set_maccuracy(meas_accuracy = enums.MeasAccuracy.HIGH) \n
		Configures the accuracy of the analysis of free-dialing single-tone sequences. \n
			:param meas_accuracy: NORMal | HIGH NORMal: lower tone detection accuracy / minimum pause length HIGH: higher tone detection accuracy / minimum pause length
		"""
		param = Conversions.enum_scalar_to_str(meas_accuracy, enums.MeasAccuracy)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:MACCuracy {param}')

	def clone(self) -> 'Fdialing':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fdialing(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
