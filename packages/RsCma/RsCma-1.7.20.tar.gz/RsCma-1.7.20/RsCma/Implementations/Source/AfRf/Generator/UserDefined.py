from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserDefined:
	"""UserDefined commands group definition. 14 total commands, 0 Subgroups, 14 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("userDefined", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.userDefined.get_enable() \n
		Enables or disables FSK modulation of user-defined data on the RF carrier. \n
			:return: undefined_enable: No help available
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:UDEFined:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, undefined_enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:ENABle \n
		Snippet: driver.source.afRf.generator.userDefined.set_enable(undefined_enable = False) \n
		Enables or disables FSK modulation of user-defined data on the RF carrier. \n
			:param undefined_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(undefined_enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:UDEFined:ENABle {param}')

	def get_imodulation(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:IMODulation \n
		Snippet: value: bool = driver.source.afRf.generator.userDefined.get_imodulation() \n
		Inverts the frequency deviation of the symbols for the frequency-shift keying modulation. \n
			:return: imod: OFF | ON
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:IMODulation?')
		return Conversions.str_to_bool(response)

	def set_imodulation(self, imod: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:IMODulation \n
		Snippet: driver.source.afRf.generator.userDefined.set_imodulation(imod = False) \n
		Inverts the frequency deviation of the symbols for the frequency-shift keying modulation. \n
			:param imod: OFF | ON
		"""
		param = Conversions.bool_to_str(imod)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:IMODulation {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.RepeatMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:REPetition \n
		Snippet: value: enums.RepeatMode = driver.source.afRf.generator.userDefined.get_repetition() \n
		Specifies how often the bit sequence is processed for the user-defined standard. \n
			:return: repetition: CONTinuous | SINGle SINGleshot: Single transmission of the bit sequence CONTinuous: Continuous repetition of the bit sequence
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.RepeatMode)

	def set_repetition(self, repetition: enums.RepeatMode) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:REPetition \n
		Snippet: driver.source.afRf.generator.userDefined.set_repetition(repetition = enums.RepeatMode.CONTinuous) \n
		Specifies how often the bit sequence is processed for the user-defined standard. \n
			:param repetition: CONTinuous | SINGle SINGleshot: Single transmission of the bit sequence CONTinuous: Continuous repetition of the bit sequence
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.RepeatMode)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:REPetition {param}')

	def get_pause(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:PAUSe \n
		Snippet: value: float = driver.source.afRf.generator.userDefined.get_pause() \n
		Defines the duration of a pause between two repetitions of a bit sequence for the user-defined standard. \n
			:return: pause: Range: 0 ms to 10E+3 ms, Unit: s
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:PAUSe?')
		return Conversions.str_to_float(response)

	def set_pause(self, pause: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:PAUSe \n
		Snippet: driver.source.afRf.generator.userDefined.set_pause(pause = 1.0) \n
		Defines the duration of a pause between two repetitions of a bit sequence for the user-defined standard. \n
			:param pause: Range: 0 ms to 10E+3 ms, Unit: s
		"""
		param = Conversions.decimal_value_to_str(pause)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:PAUSe {param}')

	def get_bandwidth(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:BANDwidth \n
		Snippet: value: float = driver.source.afRf.generator.userDefined.get_bandwidth() \n
		Selects the bandwidth of the 'Gauss' filter for pulse shaping for the user-defined standard. \n
			:return: bandwidth: Range: 1000 Hz to 100000 Hz
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:BANDwidth?')
		return Conversions.str_to_float(response)

	def set_bandwidth(self, bandwidth: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:BANDwidth \n
		Snippet: driver.source.afRf.generator.userDefined.set_bandwidth(bandwidth = 1.0) \n
		Selects the bandwidth of the 'Gauss' filter for pulse shaping for the user-defined standard. \n
			:param bandwidth: Range: 1000 Hz to 100000 Hz
		"""
		param = Conversions.decimal_value_to_str(bandwidth)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:BANDwidth {param}')

	# noinspection PyTypeChecker
	def get_ilength(self) -> enums.ImpulseLength:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:ILENgth \n
		Snippet: value: enums.ImpulseLength = driver.source.afRf.generator.userDefined.get_ilength() \n
		Selects the impulse length of the filter used for pulse shaping for the user-defined standard. \n
			:return: impulse_length: T | T2 | T4 | T6 | T8
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:ILENgth?')
		return Conversions.str_to_scalar_enum(response, enums.ImpulseLength)

	def set_ilength(self, impulse_length: enums.ImpulseLength) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:ILENgth \n
		Snippet: driver.source.afRf.generator.userDefined.set_ilength(impulse_length = enums.ImpulseLength.T) \n
		Selects the impulse length of the filter used for pulse shaping for the user-defined standard. \n
			:param impulse_length: T | T2 | T4 | T6 | T8
		"""
		param = Conversions.enum_scalar_to_str(impulse_length, enums.ImpulseLength)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:ILENgth {param}')

	def get_ro_factor(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:ROFactor \n
		Snippet: value: float = driver.source.afRf.generator.userDefined.get_ro_factor() \n
		Specifies the roll-off factor of the filter used for pulse shaping for the user-defined standard. \n
			:return: ro_factor: Range: 0 to 1
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:ROFactor?')
		return Conversions.str_to_float(response)

	def set_ro_factor(self, ro_factor: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:ROFactor \n
		Snippet: driver.source.afRf.generator.userDefined.set_ro_factor(ro_factor = 1.0) \n
		Specifies the roll-off factor of the filter used for pulse shaping for the user-defined standard. \n
			:param ro_factor: Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(ro_factor)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:ROFactor {param}')

	# noinspection PyTypeChecker
	def get_filter_py(self) -> enums.GeneratorFilter:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:FILTer \n
		Snippet: value: enums.GeneratorFilter = driver.source.afRf.generator.userDefined.get_filter_py() \n
		Selects a filter type for pulse shaping for the user-defined standard. \n
			:return: filter_py: GAUSs | RRC | RC | COS | SINC
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:FILTer?')
		return Conversions.str_to_scalar_enum(response, enums.GeneratorFilter)

	def set_filter_py(self, filter_py: enums.GeneratorFilter) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:FILTer \n
		Snippet: driver.source.afRf.generator.userDefined.set_filter_py(filter_py = enums.GeneratorFilter.COS) \n
		Selects a filter type for pulse shaping for the user-defined standard. \n
			:param filter_py: GAUSs | RRC | RC | COS | SINC
		"""
		param = Conversions.enum_scalar_to_str(filter_py, enums.GeneratorFilter)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:FILTer {param}')

	def get_slength(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:SLENgth \n
		Snippet: value: int = driver.source.afRf.generator.userDefined.get_slength() \n
		Specifies the length of a single bit sequence for the user-defined standard. \n
			:return: slength: Range: 0 bits to 16320 bits, Unit: bits
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:SLENgth \n
		Snippet: driver.source.afRf.generator.userDefined.set_slength(slength = 1) \n
		Specifies the length of a single bit sequence for the user-defined standard. \n
			:param slength: Range: 0 bits to 16320 bits, Unit: bits
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:SLENgth {param}')

	def get_drate(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:DRATe \n
		Snippet: value: int = driver.source.afRf.generator.userDefined.get_drate() \n
		Specifies the data rate for the user-defined standard. \n
			:return: drate: Range: 200 bit/s to 115200 bit/s, Unit: bit/s
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:DRATe?')
		return Conversions.str_to_int(response)

	def set_drate(self, drate: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:DRATe \n
		Snippet: driver.source.afRf.generator.userDefined.set_drate(drate = 1) \n
		Specifies the data rate for the user-defined standard. \n
			:param drate: Range: 200 bit/s to 115200 bit/s, Unit: bit/s
		"""
		param = Conversions.decimal_value_to_str(drate)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:DRATe {param}')

	def get_svalue(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:SVALue \n
		Snippet: value: str = driver.source.afRf.generator.userDefined.get_svalue() \n
		Specifies the seed value for the PRBS generator, for the user-defined standard. \n
			:return: svalue: Range: #H0 to #H1FF (for PRBS 6 max. #H3F)
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:SVALue?')
		return trim_str_response(response)

	def set_svalue(self, svalue: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:SVALue \n
		Snippet: driver.source.afRf.generator.userDefined.set_svalue(svalue = r1) \n
		Specifies the seed value for the PRBS generator, for the user-defined standard. \n
			:param svalue: Range: #H0 to #H1FF (for PRBS 6 max. #H3F)
		"""
		param = Conversions.value_to_str(svalue)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:SVALue {param}')

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.UserDefPattern:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:PATTern \n
		Snippet: value: enums.UserDefPattern = driver.source.afRf.generator.userDefined.get_pattern() \n
		Selects the bit pattern to be transmitted as payload for the user-defined standard. \n
			:return: pattern: PRBS6 | PRBS9
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.UserDefPattern)

	def set_pattern(self, pattern: enums.UserDefPattern) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:PATTern \n
		Snippet: driver.source.afRf.generator.userDefined.set_pattern(pattern = enums.UserDefPattern.PRBS6) \n
		Selects the bit pattern to be transmitted as payload for the user-defined standard. \n
			:param pattern: PRBS6 | PRBS9
		"""
		param = Conversions.enum_scalar_to_str(pattern, enums.UserDefPattern)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:PATTern {param}')

	def get_standard_dev(self) -> List[float]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:SDEViation \n
		Snippet: value: List[float] = driver.source.afRf.generator.userDefined.get_standard_dev() \n
		Defines the frequency deviations for the frequency-shift keying modulation (2FSK, 4FSK) of the user-defined standard.
		A setting command defines the deviation for symbol 01. The deviations for the other symbols are calculated from the
		setting. A query returns a comma-separated list of four deviations, for symbol 01, 00, 10, 11. \n
			:return: sdeviation: Frequency deviation Range: 0 Hz to 100 kHz, Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_float_list_with_opc('SOURce:AFRF:GENerator<Instance>:UDEFined:SDEViation?')
		return response

	def set_standard_dev(self, sdeviation: List[float]) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:SDEViation \n
		Snippet: driver.source.afRf.generator.userDefined.set_standard_dev(sdeviation = [1.1, 2.2, 3.3]) \n
		Defines the frequency deviations for the frequency-shift keying modulation (2FSK, 4FSK) of the user-defined standard.
		A setting command defines the deviation for symbol 01. The deviations for the other symbols are calculated from the
		setting. A query returns a comma-separated list of four deviations, for symbol 01, 00, 10, 11. \n
			:param sdeviation: Frequency deviation Range: 0 Hz to 100 kHz, Unit: Hz
		"""
		param = Conversions.list_to_csv_str(sdeviation)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:UDEFined:SDEViation {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FskMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:MODE \n
		Snippet: value: enums.FskMode = driver.source.afRf.generator.userDefined.get_mode() \n
		Sets the frequency-shift keying modulation type for the user-defined generator setting. \n
			:return: mode: FSK2 | FSK4
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:UDEFined:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FskMode)

	def set_mode(self, mode: enums.FskMode) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:UDEFined:MODE \n
		Snippet: driver.source.afRf.generator.userDefined.set_mode(mode = enums.FskMode.FSK2) \n
		Sets the frequency-shift keying modulation type for the user-defined generator setting. \n
			:param mode: FSK2 | FSK4
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.FskMode)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:UDEFined:MODE {param}')
