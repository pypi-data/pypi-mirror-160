from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tsensitivity:
	"""Tsensitivity commands group definition. 6 total commands, 0 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tsensitivity", core, parent)

	def get_trelative(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TRELative \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.tsensitivity.get_trelative() \n
		Configures the relative target value of target deviation depending on the modulation technique. \n
			:return: target_relative: Unit: %
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TRELative?')
		return Conversions.str_to_float(response)

	def set_trelative(self, target_relative: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TRELative \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tsensitivity.set_trelative(target_relative = 1.0) \n
		Configures the relative target value of target deviation depending on the modulation technique. \n
			:param target_relative: Unit: %
		"""
		param = Conversions.decimal_value_to_str(target_relative)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TRELative {param}')

	def get_tf_deviation(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TFDeviation \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.tsensitivity.get_tf_deviation() \n
		Specify the target deviation of the modulation signal of the DUT. Depending on the used modulation technique, the system
		deviation can be frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:return: target_freq_dev: Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TFDeviation?')
		return Conversions.str_to_float(response)

	def set_tf_deviation(self, target_freq_dev: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TFDeviation \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tsensitivity.set_tf_deviation(target_freq_dev = 1.0) \n
		Specify the target deviation of the modulation signal of the DUT. Depending on the used modulation technique, the system
		deviation can be frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:param target_freq_dev: Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(target_freq_dev)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TFDeviation {param}')

	def get_tp_deviation(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TPDeviation \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.tsensitivity.get_tp_deviation() \n
		Specify the target deviation of the modulation signal of the DUT. Depending on the used modulation technique, the system
		deviation can be frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:return: target_phase_dev: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TPDeviation?')
		return Conversions.str_to_float(response)

	def set_tp_deviation(self, target_phase_dev: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TPDeviation \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tsensitivity.set_tp_deviation(target_phase_dev = 1.0) \n
		Specify the target deviation of the modulation signal of the DUT. Depending on the used modulation technique, the system
		deviation can be frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:param target_phase_dev: Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(target_phase_dev)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TPDeviation {param}')

	def get_tm_depth(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TMDepth \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.tsensitivity.get_tm_depth() \n
		Specify the target deviation of the modulation signal of the DUT. Depending on the used modulation technique, the system
		deviation can be frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:return: target_mod_depth: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TMDepth?')
		return Conversions.str_to_float(response)

	def set_tm_depth(self, target_mod_depth: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TMDepth \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tsensitivity.set_tm_depth(target_mod_depth = 1.0) \n
		Specify the target deviation of the modulation signal of the DUT. Depending on the used modulation technique, the system
		deviation can be frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:param target_mod_depth: Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(target_mod_depth)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TMDepth {param}')

	def get_ttolerance(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TTOLerance \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.tsensitivity.get_ttolerance() \n
		Configures the maximum allowed deviation of the current target deviation of the demodulated signal. \n
			:return: tolerance: Unit: %
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TTOLerance?')
		return Conversions.str_to_float(response)

	def set_ttolerance(self, tolerance: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TTOLerance \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tsensitivity.set_ttolerance(tolerance = 1.0) \n
		Configures the maximum allowed deviation of the current target deviation of the demodulated signal. \n
			:param tolerance: Unit: %
		"""
		param = Conversions.decimal_value_to_str(tolerance)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TTOLerance {param}')

	# noinspection PyTypeChecker
	def get_tparameter(self) -> enums.TargetParameter:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TPARameter \n
		Snippet: value: enums.TargetParameter = driver.configure.afRf.measurement.searchRoutines.tsensitivity.get_tparameter() \n
		Configures the target parameter for the deviation value of the demodulated signal. \n
			:return: target_parameter: RMS | RMSQ | PPEK | NPEK | PNPA RMS 'RMS' RMSQ 'RMS*Sqrt(2) ' PPEK 'PeakPositive' NPEK 'PeakNegative' PNPA 'PosNegPeakAvg'
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TPARameter?')
		return Conversions.str_to_scalar_enum(response, enums.TargetParameter)

	def set_tparameter(self, target_parameter: enums.TargetParameter) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TPARameter \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tsensitivity.set_tparameter(target_parameter = enums.TargetParameter.NPEK) \n
		Configures the target parameter for the deviation value of the demodulated signal. \n
			:param target_parameter: RMS | RMSQ | PPEK | NPEK | PNPA RMS 'RMS' RMSQ 'RMS*Sqrt(2) ' PPEK 'PeakPositive' NPEK 'PeakNegative' PNPA 'PosNegPeakAvg'
		"""
		param = Conversions.enum_scalar_to_str(target_parameter, enums.TargetParameter)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:TPARameter {param}')
