from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tx:
	"""Tx commands group definition. 8 total commands, 1 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tx", core, parent)

	@property
	def demod(self):
		"""demod commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_demod'):
			from .Demod import Demod
			self._demod = Demod(self._core, self._cmd_group)
		return self._demod

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SearchRoutine:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:MODE \n
		Snippet: value: enums.SearchRoutine = driver.configure.afRf.measurement.searchRoutines.tx.get_mode() \n
		Selects the TX search routine to be performed. \n
			:return: search_routine: TSENsitivity | SSNR TSENsitivity 'TX Modulation Sensitivity' SSNR 'Switched SNR'
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SearchRoutine)

	def set_mode(self, search_routine: enums.SearchRoutine) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:MODE \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tx.set_mode(search_routine = enums.SearchRoutine.ADELay) \n
		Selects the TX search routine to be performed. \n
			:param search_routine: TSENsitivity | SSNR TSENsitivity 'TX Modulation Sensitivity' SSNR 'Switched SNR'
		"""
		param = Conversions.enum_scalar_to_str(search_routine, enums.SearchRoutine)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:MODE {param}')

	def get_se_time(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:SETime \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.tx.get_se_time() \n
		Specifies the waiting time after a change of the signal properties before the measurement is started. \n
			:return: setting_time: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:SETime?')
		return Conversions.str_to_float(response)

	def set_se_time(self, setting_time: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:SETime \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tx.set_se_time(setting_time = 1.0) \n
		Specifies the waiting time after a change of the signal properties before the measurement is started. \n
			:param setting_time: Unit: s
		"""
		param = Conversions.decimal_value_to_str(setting_time)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:SETime {param}')

	def get_mlevel(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:MLEVel \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.tx.get_mlevel() \n
		Sets the maximum AF level for the AF/VoIP signal path. \n
			:return: max_level: Unit: V
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:MLEVel?')
		return Conversions.str_to_float(response)

	def set_mlevel(self, max_level: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:MLEVel \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tx.set_mlevel(max_level = 1.0) \n
		Sets the maximum AF level for the AF/VoIP signal path. \n
			:param max_level: Unit: V
		"""
		param = Conversions.decimal_value_to_str(max_level)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:MLEVel {param}')

	# noinspection PyTypeChecker
	def get_af_source(self) -> enums.TxAfSource:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:AFSource \n
		Snippet: value: enums.TxAfSource = driver.configure.afRf.measurement.searchRoutines.tx.get_af_source() \n
		Specifies the signal path, i.e. the AF source, of the AF signal generated in the AFRF signal generator for transmission
		to the DUT \n
			:return: af_source: AF1O | AF2O | VOIP AF1O AF1 OUT AF2O AF2 OUT VOIP VoIP
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:AFSource?')
		return Conversions.str_to_scalar_enum(response, enums.TxAfSource)

	def set_af_source(self, af_source: enums.TxAfSource) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:AFSource \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tx.set_af_source(af_source = enums.TxAfSource.AF1O) \n
		Specifies the signal path, i.e. the AF source, of the AF signal generated in the AFRF signal generator for transmission
		to the DUT \n
			:param af_source: AF1O | AF2O | VOIP AF1O AF1 OUT AF2O AF2 OUT VOIP VoIP
		"""
		param = Conversions.enum_scalar_to_str(af_source, enums.TxAfSource)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:AFSource {param}')

	def get_rf_deviation(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RFDeviation \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.tx.get_rf_deviation() \n
		Specify the rated system deviation of the DUT. Depending on the used modulation technique, the system deviation can be
		frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:return: rated_freq_dev: Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RFDeviation?')
		return Conversions.str_to_float(response)

	def set_rf_deviation(self, rated_freq_dev: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RFDeviation \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tx.set_rf_deviation(rated_freq_dev = 1.0) \n
		Specify the rated system deviation of the DUT. Depending on the used modulation technique, the system deviation can be
		frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:param rated_freq_dev: Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(rated_freq_dev)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RFDeviation {param}')

	def get_rp_deviation(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RPDeviation \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.tx.get_rp_deviation() \n
		Specify the rated system deviation of the DUT. Depending on the used modulation technique, the system deviation can be
		frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:return: rated_phase_dev: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RPDeviation?')
		return Conversions.str_to_float(response)

	def set_rp_deviation(self, rated_phase_dev: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RPDeviation \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tx.set_rp_deviation(rated_phase_dev = 1.0) \n
		Specify the rated system deviation of the DUT. Depending on the used modulation technique, the system deviation can be
		frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:param rated_phase_dev: Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(rated_phase_dev)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RPDeviation {param}')

	def get_rm_depth(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RMDepth \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.tx.get_rm_depth() \n
		Specify the rated system deviation of the DUT. Depending on the used modulation technique, the system deviation can be
		frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:return: rated_mod_depth: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RMDepth?')
		return Conversions.str_to_float(response)

	def set_rm_depth(self, rated_mod_depth: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RMDepth \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tx.set_rm_depth(rated_mod_depth = 1.0) \n
		Specify the rated system deviation of the DUT. Depending on the used modulation technique, the system deviation can be
		frequency deviation (FM) , modulation depth (AM) and phase deviation (PM) . \n
			:param rated_mod_depth: Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(rated_mod_depth)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:RMDepth {param}')

	def clone(self) -> 'Tx':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tx(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
