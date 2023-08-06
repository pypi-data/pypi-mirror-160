from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tones:
	"""Tones commands group definition. 16 total commands, 3 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tones", core, parent)

	@property
	def subtone(self):
		"""subtone commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_subtone'):
			from .Subtone import Subtone
			self._subtone = Subtone(self._core, self._cmd_group)
		return self._subtone

	@property
	def ctCss(self):
		"""ctCss commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ctCss'):
			from .CtCss import CtCss
			self._ctCss = CtCss(self._core, self._cmd_group)
		return self._ctCss

	@property
	def dcs(self):
		"""dcs commands group. 2 Sub-classes, 6 commands."""
		if not hasattr(self, '_dcs'):
			from .Dcs import Dcs
			self._dcs = Dcs(self._core, self._cmd_group)
		return self._dcs

	def get_fdeviation(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:FDEViation \n
		Snippet: value: float = driver.source.afRf.generator.tones.get_fdeviation() \n
		Specifies the maximum frequency deviation, used in FM mode to add a tone to the RF carrier. \n
			:return: freq_deviation: Range: 0 Hz to 10 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:FDEViation?')
		return Conversions.str_to_float(response)

	def set_fdeviation(self, freq_deviation: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:FDEViation \n
		Snippet: driver.source.afRf.generator.tones.set_fdeviation(freq_deviation = 1.0) \n
		Specifies the maximum frequency deviation, used in FM mode to add a tone to the RF carrier. \n
			:param freq_deviation: Range: 0 Hz to 10 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(freq_deviation)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:FDEViation {param}')

	def get_pdeviation(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:PDEViation \n
		Snippet: value: float = driver.source.afRf.generator.tones.get_pdeviation() \n
		Specifies the maximum phase deviation, used in PM mode to add a tone to the RF carrier. \n
			:return: phase_deviation: Range: 0 rad to 10 rad, Unit: rad
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:PDEViation?')
		return Conversions.str_to_float(response)

	def set_pdeviation(self, phase_deviation: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:PDEViation \n
		Snippet: driver.source.afRf.generator.tones.set_pdeviation(phase_deviation = 1.0) \n
		Specifies the maximum phase deviation, used in PM mode to add a tone to the RF carrier. \n
			:param phase_deviation: Range: 0 rad to 10 rad, Unit: rad
		"""
		param = Conversions.decimal_value_to_str(phase_deviation)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:PDEViation {param}')

	def get_mod_depth(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:MDEPth \n
		Snippet: value: float = driver.source.afRf.generator.tones.get_mod_depth() \n
		Specifies the modulation depth, used in AM mode to add a tone to the RF carrier. \n
			:return: modulation_depth: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:MDEPth?')
		return Conversions.str_to_float(response)

	def set_mod_depth(self, modulation_depth: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:MDEPth \n
		Snippet: driver.source.afRf.generator.tones.set_mod_depth(modulation_depth = 1.0) \n
		Specifies the modulation depth, used in AM mode to add a tone to the RF carrier. \n
			:param modulation_depth: Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(modulation_depth)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:MDEPth {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.ToneTypeB:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes \n
		Snippet: value: enums.ToneTypeB = driver.source.afRf.generator.tones.get_value() \n
		Selects the type of additional tones to be generated. \n
			:return: tone_type: NONE | SUBTone | CTCSs | DCS NONE No additional tones SUBTone Single subtone CTCSs Single CTCSS subaudible tone DCS DCS signal
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes?')
		return Conversions.str_to_scalar_enum(response, enums.ToneTypeB)

	def set_value(self, tone_type: enums.ToneTypeB) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes \n
		Snippet: driver.source.afRf.generator.tones.set_value(tone_type = enums.ToneTypeB.CTCSs) \n
		Selects the type of additional tones to be generated. \n
			:param tone_type: NONE | SUBTone | CTCSs | DCS NONE No additional tones SUBTone Single subtone CTCSs Single CTCSS subaudible tone DCS DCS signal
		"""
		param = Conversions.enum_scalar_to_str(tone_type, enums.ToneTypeB)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes {param}')

	def clone(self) -> 'Tones':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tones(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
