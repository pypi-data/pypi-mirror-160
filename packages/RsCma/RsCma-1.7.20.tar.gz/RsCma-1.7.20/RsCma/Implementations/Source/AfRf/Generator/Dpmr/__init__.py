from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpmr:
	"""Dpmr commands group definition. 13 total commands, 1 Subgroups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dpmr", core, parent)

	@property
	def ccode(self):
		"""ccode commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ccode'):
			from .Ccode import Ccode
			self._ccode = Ccode(self._core, self._cmd_group)
		return self._ccode

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.NxdnPatternB:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:PATTern \n
		Snippet: value: enums.NxdnPatternB = driver.source.afRf.generator.dpmr.get_pattern() \n
		Selects the bit pattern to be transmitted as payload for DPMR. \n
			:return: pattern: RSYR | RLD | R1031 | RA1 | RA0 | R10A | RBRB9 | RBRB15 | CUST
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DPMR:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.NxdnPatternB)

	def set_pattern(self, pattern: enums.NxdnPatternB) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:PATTern \n
		Snippet: driver.source.afRf.generator.dpmr.set_pattern(pattern = enums.NxdnPatternB.CUST) \n
		Selects the bit pattern to be transmitted as payload for DPMR. \n
			:param pattern: RSYR | RLD | R1031 | RA1 | RA0 | R10A | RBRB9 | RBRB15 | CUST
		"""
		param = Conversions.enum_scalar_to_str(pattern, enums.NxdnPatternB)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DPMR:PATTern {param}')

	def get_svalue(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:SVALue \n
		Snippet: value: str = driver.source.afRf.generator.dpmr.get_svalue() \n
		Specifies the 9-bit seed value for the PRBS generator, for DPMR. \n
			:return: svalue: Range: #H0 to #H1FF
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DPMR:SVALue?')
		return trim_str_response(response)

	def set_svalue(self, svalue: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:SVALue \n
		Snippet: driver.source.afRf.generator.dpmr.set_svalue(svalue = r1) \n
		Specifies the 9-bit seed value for the PRBS generator, for DPMR. \n
			:param svalue: Range: #H0 to #H1FF
		"""
		param = Conversions.value_to_str(svalue)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DPMR:SVALue {param}')

	def get_sid(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:SID \n
		Snippet: value: str = driver.source.afRf.generator.dpmr.get_sid() \n
		Configures the source ID, for DPMR. \n
			:return: sid: No help available
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DPMR:SID?')
		return trim_str_response(response)

	def set_sid(self, sid: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:SID \n
		Snippet: driver.source.afRf.generator.dpmr.set_sid(sid = '1') \n
		Configures the source ID, for DPMR. \n
			:param sid: No help available
		"""
		param = Conversions.value_to_quoted_str(sid)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DPMR:SID {param}')

	def get_did(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:DID \n
		Snippet: value: str = driver.source.afRf.generator.dpmr.get_did() \n
		Configures the destination ID, for DPMR. \n
			:return: did: No help available
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DPMR:DID?')
		return trim_str_response(response)

	def set_did(self, did: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:DID \n
		Snippet: driver.source.afRf.generator.dpmr.set_did(did = '1') \n
		Configures the destination ID, for DPMR. \n
			:param did: No help available
		"""
		param = Conversions.value_to_quoted_str(did)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DPMR:DID {param}')

	def get_pt_peer(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:PTPeer \n
		Snippet: value: bool = driver.source.afRf.generator.dpmr.get_pt_peer() \n
		Configures the 'Peer to Peer' bit for the communication between DUTs (DPMR mode 1) . \n
			:return: emergency: OFF | ON
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DPMR:PTPeer?')
		return Conversions.str_to_bool(response)

	def set_pt_peer(self, emergency: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:PTPeer \n
		Snippet: driver.source.afRf.generator.dpmr.set_pt_peer(emergency = False) \n
		Configures the 'Peer to Peer' bit for the communication between DUTs (DPMR mode 1) . \n
			:param emergency: OFF | ON
		"""
		param = Conversions.bool_to_str(emergency)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DPMR:PTPeer {param}')

	def get_emergency(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:EMERgency \n
		Snippet: value: bool = driver.source.afRf.generator.dpmr.get_emergency() \n
		Configures the emergency bit to be signaled to the DUT, for DPMR. \n
			:return: emergency: OFF | ON
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DPMR:EMERgency?')
		return Conversions.str_to_bool(response)

	def set_emergency(self, emergency: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:EMERgency \n
		Snippet: driver.source.afRf.generator.dpmr.set_emergency(emergency = False) \n
		Configures the emergency bit to be signaled to the DUT, for DPMR. \n
			:param emergency: OFF | ON
		"""
		param = Conversions.bool_to_str(emergency)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DPMR:EMERgency {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FskMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:MODE \n
		Snippet: value: enums.FskMode = driver.source.afRf.generator.dpmr.get_mode() \n
		Queries the modulation type used for DPMR. \n
			:return: mode: FSK2 | FSK4
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DPMR:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FskMode)

	def get_standard_dev(self) -> List[float]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:SDEViation \n
		Snippet: value: List[float] = driver.source.afRf.generator.dpmr.get_standard_dev() \n
		Queries the frequency deviations used for 4FSK modulation, for DPMR. \n
			:return: sdeviation: List of four frequency deviations, for the symbols 01, 00, 10, 11. Range: -2000 Hz to 2000 Hz, Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_float_list_with_opc('SOURce:AFRF:GENerator<Instance>:DPMR:SDEViation?')
		return response

	def get_symbol_rate(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:SRATe \n
		Snippet: value: float = driver.source.afRf.generator.dpmr.get_symbol_rate() \n
		Queries the symbol rate for DPMR. \n
			:return: srate: Range: 0 symbol/s to 100E+6 symbol/s, Unit: bit/s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DPMR:SRATe?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_filter_py(self) -> enums.PulseShapingFilter:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:FILTer \n
		Snippet: value: enums.PulseShapingFilter = driver.source.afRf.generator.dpmr.get_filter_py() \n
		Queries the filter type used for pulse shaping for DPMR. \n
			:return: filter_py: RRC
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DPMR:FILTer?')
		return Conversions.str_to_scalar_enum(response, enums.PulseShapingFilter)

	def get_ro_factor(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:ROFactor \n
		Snippet: value: float = driver.source.afRf.generator.dpmr.get_ro_factor() \n
		Queries the roll-off factor of the filter used for pulse shaping, for DPMR. \n
			:return: ro_factor: Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DPMR:ROFactor?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Dpmr':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dpmr(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
