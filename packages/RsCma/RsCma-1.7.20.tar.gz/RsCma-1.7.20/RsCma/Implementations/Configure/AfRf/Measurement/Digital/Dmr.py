from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dmr:
	"""Dmr commands group definition. 9 total commands, 0 Subgroups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dmr", core, parent)

	# noinspection PyTypeChecker
	def get_ldirection(self) -> enums.LinkDirectionDmr:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:LDIRection \n
		Snippet: value: enums.LinkDirectionDmr = driver.configure.afRf.measurement.digital.dmr.get_ldirection() \n
		Specifies the direction of voice/data transmission. The details of the used frames depend on this selection. \n
			:return: link_dirction: MSSourced
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:LDIRection?')
		return Conversions.str_to_scalar_enum(response, enums.LinkDirectionDmr)

	def set_ldirection(self, link_dirction: enums.LinkDirectionDmr) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:LDIRection \n
		Snippet: driver.configure.afRf.measurement.digital.dmr.set_ldirection(link_dirction = enums.LinkDirectionDmr.MSSourced) \n
		Specifies the direction of voice/data transmission. The details of the used frames depend on this selection. \n
			:param link_dirction: MSSourced
		"""
		param = Conversions.enum_scalar_to_str(link_dirction, enums.LinkDirectionDmr)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:LDIRection {param}')

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.DmrPatternB:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:PATTern \n
		Snippet: value: enums.DmrPatternB = driver.configure.afRf.measurement.digital.dmr.get_pattern() \n
		Selects the bit pattern that is expected as payload. \n
			:return: pattern: P1031 | SYNC | SILence
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.DmrPatternB)

	def set_pattern(self, pattern: enums.DmrPatternB) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:PATTern \n
		Snippet: driver.configure.afRf.measurement.digital.dmr.set_pattern(pattern = enums.DmrPatternB.P1031) \n
		Selects the bit pattern that is expected as payload. \n
			:param pattern: P1031 | SYNC | SILence
		"""
		param = Conversions.enum_scalar_to_str(pattern, enums.DmrPatternB)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:PATTern {param}')

	# noinspection PyTypeChecker
	def get_ber_period(self) -> enums.BerPeriod:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:BERPeriod \n
		Snippet: value: enums.BerPeriod = driver.configure.afRf.measurement.digital.dmr.get_ber_period() \n
		Sets the number of frames for the BER measurement. \n
			:return: ber_period: F36 | F48
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:BERPeriod?')
		return Conversions.str_to_scalar_enum(response, enums.BerPeriod)

	def set_ber_period(self, ber_period: enums.BerPeriod) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:BERPeriod \n
		Snippet: driver.configure.afRf.measurement.digital.dmr.set_ber_period(ber_period = enums.BerPeriod.F36) \n
		Sets the number of frames for the BER measurement. \n
			:param ber_period: F36 | F48
		"""
		param = Conversions.enum_scalar_to_str(ber_period, enums.BerPeriod)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:BERPeriod {param}')

	# noinspection PyTypeChecker
	def get_cmode(self) -> enums.ChannelModeDmr:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:CMODe \n
		Snippet: value: enums.ChannelModeDmr = driver.configure.afRf.measurement.digital.dmr.get_cmode() \n
		Specifies if 'Voice' or 'Data' is transmitted over the radio channel. Currently, only 'Voice' is supported. \n
			:return: channel_mode: VOICe | DATA
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:CMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelModeDmr)

	# noinspection PyTypeChecker
	def get_filter_py(self) -> enums.FilterDigital:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:FILTer \n
		Snippet: value: enums.FilterDigital = driver.configure.afRf.measurement.digital.dmr.get_filter_py() \n
		Selects the filter type for pulse shaping of DMR. \n
			:return: filter_py: GAUSs | RRC | COSine | SINC
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:FILTer?')
		return Conversions.str_to_scalar_enum(response, enums.FilterDigital)

	def get_ro_factor(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:ROFactor \n
		Snippet: value: float = driver.configure.afRf.measurement.digital.dmr.get_ro_factor() \n
		Sets the roll-off factor of the filter used for pulse shaping of DMR. \n
			:return: rolloff_factor: Range: 0 to 1
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:ROFactor?')
		return Conversions.str_to_float(response)

	def get_symbol_rate(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:SRATe \n
		Snippet: value: float = driver.configure.afRf.measurement.digital.dmr.get_symbol_rate() \n
		Queries the symbol rate for DMR. \n
			:return: srate: Range: 1 symbol/s to 100E+6 symbol/s, Unit: symbol/s
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:SRATe?')
		return Conversions.str_to_float(response)

	def get_standard_dev(self) -> List[float]:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:SDEViation \n
		Snippet: value: List[float] = driver.configure.afRf.measurement.digital.dmr.get_standard_dev() \n
		Queries the frequency deviations of the 4FSK modulation for DMR. \n
			:return: sdeviation: List of four frequency deviations, for the symbols 01, 00, 10, 11. Range: -2000 Hz to 2000 Hz, Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:SDEViation?')
		return response

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.DemodulationType:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:MODE \n
		Snippet: value: enums.DemodulationType = driver.configure.afRf.measurement.digital.dmr.get_mode() \n
		Queries the modulation type used for DMR. \n
			:return: mode: FSK4
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:DMR:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DemodulationType)
