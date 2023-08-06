from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ssnr:
	"""Ssnr commands group definition. 7 total commands, 0 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ssnr", core, parent)

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.afRf.measurement.searchRoutines.ssnr.get_repetition() \n
		Selects whether the switched SNR measurement is repeated continuously or not. \n
			:return: repetition: SINGleshot | CONTinuous
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:REPetition \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.ssnr.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Selects whether the switched SNR measurement is repeated continuously or not. \n
			:param repetition: SINGleshot | CONTinuous
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:REPetition {param}')

	# noinspection PyTypeChecker
	def get_scondition(self) -> enums.StopCondition:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:SCONdition \n
		Snippet: value: enums.StopCondition = driver.configure.afRf.measurement.searchRoutines.ssnr.get_scondition() \n
		Specifies the conditions for an early termination of the measurement. \n
			:return: stop_condition: NONE | SLFail
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:SCONdition?')
		return Conversions.str_to_scalar_enum(response, enums.StopCondition)

	def set_scondition(self, stop_condition: enums.StopCondition) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:SCONdition \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.ssnr.set_scondition(stop_condition = enums.StopCondition.NONE) \n
		Specifies the conditions for an early termination of the measurement. \n
			:param stop_condition: NONE | SLFail
		"""
		param = Conversions.enum_scalar_to_str(stop_condition, enums.StopCondition)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:SCONdition {param}')

	def get_mo_exception(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:MOEXception \n
		Snippet: value: bool = driver.configure.afRf.measurement.searchRoutines.ssnr.get_mo_exception() \n
		Specifies if faulty or inaccurate switched SNR measurement results are rejected. \n
			:return: meas_on_exception: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:MOEXception?')
		return Conversions.str_to_bool(response)

	def set_mo_exception(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:MOEXception \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.ssnr.set_mo_exception(meas_on_exception = False) \n
		Specifies if faulty or inaccurate switched SNR measurement results are rejected. \n
			:param meas_on_exception: OFF | ON
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:MOEXception {param}')

	def get_scount(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:SCOunt \n
		Snippet: value: int = driver.configure.afRf.measurement.searchRoutines.ssnr.get_scount() \n
		The number of single routine runs used to evaluate the SNR. \n
			:return: statistic_count: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:SCOunt \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.ssnr.set_scount(statistic_count = 1) \n
		The number of single routine runs used to evaluate the SNR. \n
			:param statistic_count: No help available
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:SCOunt {param}')

	# noinspection PyTypeChecker
	def get_af_source(self) -> enums.AudioConnector:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:AFSource \n
		Snippet: value: enums.AudioConnector = driver.configure.afRf.measurement.searchRoutines.ssnr.get_af_source() \n
		Specifies the AF source for the switched SNR measurement. \n
			:return: af_source: AF1O | AF2O AF1 OUT or AF2 OUT
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:AFSource?')
		return Conversions.str_to_scalar_enum(response, enums.AudioConnector)

	def set_af_source(self, af_source: enums.AudioConnector) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:AFSource \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.ssnr.set_af_source(af_source = enums.AudioConnector.AF1O) \n
		Specifies the AF source for the switched SNR measurement. \n
			:param af_source: AF1O | AF2O AF1 OUT or AF2 OUT
		"""
		param = Conversions.enum_scalar_to_str(af_source, enums.AudioConnector)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:AFSource {param}')

	def get_crepetition(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:CREPetition \n
		Snippet: value: bool = driver.configure.afRf.measurement.searchRoutines.ssnr.get_crepetition() \n
		Sets the repetition mode for switched SNR measurements to 'Continuous'. \n
			:return: continuous_repetition: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:CREPetition?')
		return Conversions.str_to_bool(response)

	def set_crepetition(self, continuous_repetition: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:CREPetition \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.ssnr.set_crepetition(continuous_repetition = False) \n
		Sets the repetition mode for switched SNR measurements to 'Continuous'. \n
			:param continuous_repetition: OFF | ON
		"""
		param = Conversions.bool_to_str(continuous_repetition)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:CREPetition {param}')

	def get_rcoupling(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:RCOupling \n
		Snippet: value: bool = driver.configure.afRf.measurement.searchRoutines.ssnr.get_rcoupling() \n
		Couples the repetition mode of all switched SNR measurements. \n
			:return: repetition_coupling: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:RCOupling?')
		return Conversions.str_to_bool(response)

	def set_rcoupling(self, repetition_coupling: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:RCOupling \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.ssnr.set_rcoupling(repetition_coupling = False) \n
		Couples the repetition mode of all switched SNR measurements. \n
			:param repetition_coupling: OFF | ON
		"""
		param = Conversions.bool_to_str(repetition_coupling)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:SSNR:RCOupling {param}')
