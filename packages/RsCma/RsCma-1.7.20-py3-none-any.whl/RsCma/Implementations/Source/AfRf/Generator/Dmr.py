from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmr:
	"""Dmr commands group definition. 10 total commands, 0 Subgroups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmr", core, parent)

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.DmrPattern:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:PATTern \n
		Snippet: value: enums.DmrPattern = driver.source.afRf.generator.dmr.get_pattern() \n
		Selects the bit pattern to be transmitted as payload for DMR. \n
			:return: pattern: RSYR | RLD | RFMS | RFBS | RA1 | RA0 | R10A | RBRB9 | RBRB15
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DMR:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.DmrPattern)

	def set_pattern(self, pattern: enums.DmrPattern) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:PATTern \n
		Snippet: driver.source.afRf.generator.dmr.set_pattern(pattern = enums.DmrPattern.BPRB15) \n
		Selects the bit pattern to be transmitted as payload for DMR. \n
			:param pattern: RSYR | RLD | RFMS | RFBS | RA1 | RA0 | R10A | RBRB9 | RBRB15
		"""
		param = Conversions.enum_scalar_to_str(pattern, enums.DmrPattern)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DMR:PATTern {param}')

	def get_svalue(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:SVALue \n
		Snippet: value: str = driver.source.afRf.generator.dmr.get_svalue() \n
		Specifies the 9-bit seed value for the PRBS generator, for DMR. \n
			:return: svalue: Range: #H0 to #H1FF
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DMR:SVALue?')
		return trim_str_response(response)

	def set_svalue(self, svalue: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:SVALue \n
		Snippet: driver.source.afRf.generator.dmr.set_svalue(svalue = r1) \n
		Specifies the 9-bit seed value for the PRBS generator, for DMR. \n
			:param svalue: Range: #H0 to #H1FF
		"""
		param = Conversions.value_to_str(svalue)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DMR:SVALue {param}')

	def get_ccode(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:CCODe \n
		Snippet: value: int = driver.source.afRf.generator.dmr.get_ccode() \n
		Defines the color code to be signaled to the DUT, for DMR. \n
			:return: ccode: Range: 0 to 15
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DMR:CCODe?')
		return Conversions.str_to_int(response)

	def set_ccode(self, ccode: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:CCODe \n
		Snippet: driver.source.afRf.generator.dmr.set_ccode(ccode = 1) \n
		Defines the color code to be signaled to the DUT, for DMR. \n
			:param ccode: Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(ccode)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DMR:CCODe {param}')

	def get_saddress(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:SADDress \n
		Snippet: value: float = driver.source.afRf.generator.dmr.get_saddress() \n
		Configures the source address to be signaled to the DUT, for DMR. \n
			:return: saddress: Range: 0 to 16777215
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DMR:SADDress?')
		return Conversions.str_to_float(response)

	def set_saddress(self, saddress: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:SADDress \n
		Snippet: driver.source.afRf.generator.dmr.set_saddress(saddress = 1.0) \n
		Configures the source address to be signaled to the DUT, for DMR. \n
			:param saddress: Range: 0 to 16777215
		"""
		param = Conversions.decimal_value_to_str(saddress)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DMR:SADDress {param}')

	def get_gaddress(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:GADDress \n
		Snippet: value: float = driver.source.afRf.generator.dmr.get_gaddress() \n
		Configures the group address to be signaled to the DUT, for DMR. \n
			:return: gaddress: Range: 0 to 16777215
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DMR:GADDress?')
		return Conversions.str_to_float(response)

	def set_gaddress(self, gaddress: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:GADDress \n
		Snippet: driver.source.afRf.generator.dmr.set_gaddress(gaddress = 1.0) \n
		Configures the group address to be signaled to the DUT, for DMR. \n
			:param gaddress: Range: 0 to 16777215
		"""
		param = Conversions.decimal_value_to_str(gaddress)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DMR:GADDress {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FskMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:MODE \n
		Snippet: value: enums.FskMode = driver.source.afRf.generator.dmr.get_mode() \n
		Queries the modulation type used for DMR. \n
			:return: mode: FSK4
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DMR:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FskMode)

	def get_standard_dev(self) -> List[float]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:SDEViation \n
		Snippet: value: List[float] = driver.source.afRf.generator.dmr.get_standard_dev() \n
		Queries the frequency deviations used for 4FSK modulation, for DMR. \n
			:return: sdeviation: List of four frequency deviations, for the symbols 01, 00, 10, 11. Range: -2000 Hz to 2000 Hz, Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_float_list_with_opc('SOURce:AFRF:GENerator<Instance>:DMR:SDEViation?')
		return response

	def get_symbol_rate(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:SRATe \n
		Snippet: value: float = driver.source.afRf.generator.dmr.get_symbol_rate() \n
		Queries the symbol rate for DMR. \n
			:return: srate: Range: 4800 symbol/s to 4800 symbol/s , Unit: symbol/s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DMR:SRATe?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_filter_py(self) -> enums.PulseShapingFilter:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:FILTer \n
		Snippet: value: enums.PulseShapingFilter = driver.source.afRf.generator.dmr.get_filter_py() \n
		Queries the filter type used for pulse shaping for DMR. \n
			:return: filter_py: RRC
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DMR:FILTer?')
		return Conversions.str_to_scalar_enum(response, enums.PulseShapingFilter)

	def get_ro_factor(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DMR:ROFactor \n
		Snippet: value: float = driver.source.afRf.generator.dmr.get_ro_factor() \n
		Queries the roll-off factor of the filter used for pulse shaping for DMR. \n
			:return: ro_factor: Range: 0.2 to 0.2
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DMR:ROFactor?')
		return Conversions.str_to_float(response)
