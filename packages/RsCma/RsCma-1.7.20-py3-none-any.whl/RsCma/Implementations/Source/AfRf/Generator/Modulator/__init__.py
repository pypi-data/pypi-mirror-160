from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulator:
	"""Modulator commands group definition. 9 total commands, 2 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("modulator", core, parent)

	@property
	def fmStereo(self):
		"""fmStereo commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_fmStereo'):
			from .FmStereo import FmStereo
			self._fmStereo = FmStereo(self._core, self._cmd_group)
		return self._fmStereo

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import Enable
			self._enable = Enable(self._core, self._cmd_group)
		return self._enable

	def get_fdeviation(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:FDEViation \n
		Snippet: value: float = driver.source.afRf.generator.modulator.get_fdeviation() \n
		Specifies the maximum frequency deviation for the FM modulation scheme. \n
			:return: freq_deviation: Range: 0 Hz to 100 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:MODulator:FDEViation?')
		return Conversions.str_to_float(response)

	def set_fdeviation(self, freq_deviation: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:FDEViation \n
		Snippet: driver.source.afRf.generator.modulator.set_fdeviation(freq_deviation = 1.0) \n
		Specifies the maximum frequency deviation for the FM modulation scheme. \n
			:param freq_deviation: Range: 0 Hz to 100 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(freq_deviation)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:MODulator:FDEViation {param}')

	def get_pdeviation(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:PDEViation \n
		Snippet: value: float = driver.source.afRf.generator.modulator.get_pdeviation() \n
		Specifies the maximum phase deviation for the PM modulation scheme. \n
			:return: phase_deviation: Range: 0 rad to 10 rad, Unit: rad
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:MODulator:PDEViation?')
		return Conversions.str_to_float(response)

	def set_pdeviation(self, phase_deviation: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:PDEViation \n
		Snippet: driver.source.afRf.generator.modulator.set_pdeviation(phase_deviation = 1.0) \n
		Specifies the maximum phase deviation for the PM modulation scheme. \n
			:param phase_deviation: Range: 0 rad to 10 rad, Unit: rad
		"""
		param = Conversions.decimal_value_to_str(phase_deviation)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:MODulator:PDEViation {param}')

	def get_mod_depth(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:MDEPth \n
		Snippet: value: float = driver.source.afRf.generator.modulator.get_mod_depth() \n
		Specifies the modulation depth for the AM modulation scheme. \n
			:return: modulation_depth: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:MODulator:MDEPth?')
		return Conversions.str_to_float(response)

	def set_mod_depth(self, modulation_depth: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:MDEPth \n
		Snippet: driver.source.afRf.generator.modulator.set_mod_depth(modulation_depth = 1.0) \n
		Specifies the modulation depth for the AM modulation scheme. \n
			:param modulation_depth: Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(modulation_depth)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:MODulator:MDEPth {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.SignalSource:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator \n
		Snippet: value: enums.SignalSource = driver.source.afRf.generator.modulator.get_value() \n
		Selects the source of an audio signal to be transported via the RF carrier. \n
			:return: modulator_source: GEN3 | GEN4 | GENB | AFI1 | AFI2 | AFIB | SPIL | SPIR | SPIN GEN3 Audio generator 3 GEN4 Audio generator 4 GENB Audio generator 3 and 4 AFI1 AF1 IN AFI2 AF2 IN AFIB AF1 IN and AF2 IN SPIL SPDIF IN, left channel SPIR SPDIF IN, right channel SPIN SPDIF IN, both channels
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:MODulator?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSource)

	def set_value(self, modulator_source: enums.SignalSource) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator \n
		Snippet: driver.source.afRf.generator.modulator.set_value(modulator_source = enums.SignalSource.AFI1) \n
		Selects the source of an audio signal to be transported via the RF carrier. \n
			:param modulator_source: GEN3 | GEN4 | GENB | AFI1 | AFI2 | AFIB | SPIL | SPIR | SPIN GEN3 Audio generator 3 GEN4 Audio generator 4 GENB Audio generator 3 and 4 AFI1 AF1 IN AFI2 AF2 IN AFIB AF1 IN and AF2 IN SPIL SPDIF IN, left channel SPIR SPDIF IN, right channel SPIN SPDIF IN, both channels
		"""
		param = Conversions.enum_scalar_to_str(modulator_source, enums.SignalSource)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:MODulator {param}')

	def clone(self) -> 'Modulator':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Modulator(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
