from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nxdn:
	"""Nxdn commands group definition. 11 total commands, 0 Subgroups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nxdn", core, parent)

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.NxdnPattern:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:PATTern \n
		Snippet: value: enums.NxdnPattern = driver.source.afRf.generator.nxdn.get_pattern() \n
		Selects the bit pattern to be transmitted as payload for NXDN. \n
			:return: pattern: P1031 | P1011 | SILence | PRBS9 | PRBS15 | RSYR | RLD | RAW1 | RAW2 | RA1 | RA0 | R10A | RPRB9 | RPRB15
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:NXDN:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.NxdnPattern)

	def set_pattern(self, pattern: enums.NxdnPattern) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:PATTern \n
		Snippet: driver.source.afRf.generator.nxdn.set_pattern(pattern = enums.NxdnPattern.P1011) \n
		Selects the bit pattern to be transmitted as payload for NXDN. \n
			:param pattern: P1031 | P1011 | SILence | PRBS9 | PRBS15 | RSYR | RLD | RAW1 | RAW2 | RA1 | RA0 | R10A | RPRB9 | RPRB15
		"""
		param = Conversions.enum_scalar_to_str(pattern, enums.NxdnPattern)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:NXDN:PATTern {param}')

	def get_svalue(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:SVALue \n
		Snippet: value: str = driver.source.afRf.generator.nxdn.get_svalue() \n
		Specifies the seed value for the PRBS generator, for NXDN. \n
			:return: svalue: Range: #H0 to #H1FF
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:NXDN:SVALue?')
		return trim_str_response(response)

	def set_svalue(self, svalue: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:SVALue \n
		Snippet: driver.source.afRf.generator.nxdn.set_svalue(svalue = r1) \n
		Specifies the seed value for the PRBS generator, for NXDN. \n
			:param svalue: Range: #H0 to #H1FF
		"""
		param = Conversions.value_to_str(svalue)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:NXDN:SVALue {param}')

	def get_ran(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:RAN \n
		Snippet: value: str = driver.source.afRf.generator.nxdn.get_ran() \n
		Configures the radio access number to be signaled to the DUT, for NXDN. \n
			:return: ran: Range: #H0 to #H3F
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:NXDN:RAN?')
		return trim_str_response(response)

	def set_ran(self, ran: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:RAN \n
		Snippet: driver.source.afRf.generator.nxdn.set_ran(ran = r1) \n
		Configures the radio access number to be signaled to the DUT, for NXDN. \n
			:param ran: Range: #H0 to #H3F
		"""
		param = Conversions.value_to_str(ran)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:NXDN:RAN {param}')

	def get_suid(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:SUID \n
		Snippet: value: str = driver.source.afRf.generator.nxdn.get_suid() \n
		Configures the sender ID to be signaled to the DUT, for NXDN. \n
			:return: suid: Range: #H0 to #HFFFF
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:NXDN:SUID?')
		return trim_str_response(response)

	def set_suid(self, suid: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:SUID \n
		Snippet: driver.source.afRf.generator.nxdn.set_suid(suid = r1) \n
		Configures the sender ID to be signaled to the DUT, for NXDN. \n
			:param suid: Range: #H0 to #HFFFF
		"""
		param = Conversions.value_to_str(suid)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:NXDN:SUID {param}')

	def get_duid(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:DUID \n
		Snippet: value: str = driver.source.afRf.generator.nxdn.get_duid() \n
		Configures the destination ID to be signaled to the DUT, for NXDN. \n
			:return: duid: Range: #H0 to #HFFFF
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:NXDN:DUID?')
		return trim_str_response(response)

	def set_duid(self, duid: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:DUID \n
		Snippet: driver.source.afRf.generator.nxdn.set_duid(duid = r1) \n
		Configures the destination ID to be signaled to the DUT, for NXDN. \n
			:param duid: Range: #H0 to #HFFFF
		"""
		param = Conversions.value_to_str(duid)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:NXDN:DUID {param}')

	# noinspection PyTypeChecker
	def get_transmission(self) -> enums.Transmission:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:TRANsmission \n
		Snippet: value: enums.Transmission = driver.source.afRf.generator.nxdn.get_transmission() \n
		Selects the transmission mode for NXDN. \n
			:return: trans: EHR4800 | EHR9600 | EFR9600 Enhanced half-rate (EHR) or full-rate (EFR) speech codec Transmission rate 4800 bps or 9600 bps
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:NXDN:TRANsmission?')
		return Conversions.str_to_scalar_enum(response, enums.Transmission)

	def set_transmission(self, trans: enums.Transmission) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:TRANsmission \n
		Snippet: driver.source.afRf.generator.nxdn.set_transmission(trans = enums.Transmission.EFR9600) \n
		Selects the transmission mode for NXDN. \n
			:param trans: EHR4800 | EHR9600 | EFR9600 Enhanced half-rate (EHR) or full-rate (EFR) speech codec Transmission rate 4800 bps or 9600 bps
		"""
		param = Conversions.enum_scalar_to_str(trans, enums.Transmission)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:NXDN:TRANsmission {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FskMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:MODE \n
		Snippet: value: enums.FskMode = driver.source.afRf.generator.nxdn.get_mode() \n
		Queries the modulation type used for NXDN. \n
			:return: mode: FSK4
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:NXDN:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FskMode)

	def get_standard_dev(self) -> List[float]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:SDEViation \n
		Snippet: value: List[float] = driver.source.afRf.generator.nxdn.get_standard_dev() \n
		Queries the frequency deviations used for 4FSK modulation, for NXDN. \n
			:return: sdeviation: List of four frequency deviations, for the symbols 01, 00, 10, 11. Range: -3000 Hz to 3000 Hz, Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_float_list('SOURce:AFRF:GENerator<Instance>:NXDN:SDEViation?')
		return response

	def get_symbol_rate(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:SRATe \n
		Snippet: value: float = driver.source.afRf.generator.nxdn.get_symbol_rate() \n
		Queries the symbol rate resulting from the configured transmission mode, for NXDN. \n
			:return: srate: Range: 0 symbol/s to 100E+6 symbol/s, Unit: symbol/s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:NXDN:SRATe?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_filter_py(self) -> enums.FilterNxDn:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:FILTer \n
		Snippet: value: enums.FilterNxDn = driver.source.afRf.generator.nxdn.get_filter_py() \n
		Queries the filter type used for pulse shaping for NXDN. \n
			:return: filter_py: NXTX
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:NXDN:FILTer?')
		return Conversions.str_to_scalar_enum(response, enums.FilterNxDn)

	def get_ro_factor(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:NXDN:ROFactor \n
		Snippet: value: float = driver.source.afRf.generator.nxdn.get_ro_factor() \n
		Queries the roll-off factor of the filter used for pulse shaping for NXDN. \n
			:return: ro_factor: Range: 0.2 to 0.2
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:NXDN:ROFactor?')
		return Conversions.str_to_float(response)
