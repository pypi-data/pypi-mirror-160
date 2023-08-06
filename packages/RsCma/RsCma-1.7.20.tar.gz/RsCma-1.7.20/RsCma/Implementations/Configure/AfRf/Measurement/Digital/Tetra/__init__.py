from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tetra:
	"""Tetra commands group definition. 16 total commands, 1 Subgroups, 13 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tetra", core, parent)

	@property
	def uplink(self):
		"""uplink commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_uplink'):
			from .Uplink import Uplink
			self._uplink = Uplink(self._core, self._cmd_group)
		return self._uplink

	def get_symbol_rate(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:SRATe \n
		Snippet: value: float = driver.configure.afRf.measurement.digital.tetra.get_symbol_rate() \n
		Queries the symbol rate for TETRA. \n
			:return: srate: Unit: symbol/s
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:SRATe?')
		return Conversions.str_to_float(response)

	def get_standard_dev(self) -> List[str]:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:SDEViation \n
		Snippet: value: List[str] = driver.configure.afRf.measurement.digital.tetra.get_standard_dev() \n
		Queries the phase changes of the DQPSK modulation for TETRA. \n
			:return: sdeviation: List of four phase changes, for the symbols 01, 00, 10, 11.
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:SDEViation?')
		return Conversions.str_to_str_list(response)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.ModeTetra:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:MODE \n
		Snippet: value: enums.ModeTetra = driver.configure.afRf.measurement.digital.tetra.get_mode() \n
		Queries the modulation type used for TETRA. \n
			:return: mode: DQPSK
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.ModeTetra)

	# noinspection PyTypeChecker
	def get_ldirection(self) -> enums.LinkDirectionTetra:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:LDIRection \n
		Snippet: value: enums.LinkDirectionTetra = driver.configure.afRf.measurement.digital.tetra.get_ldirection() \n
		Sets either the Downlink/forward or the uplink/backward direction of the test. The downlink direction is from BS to MS,
		the uplink direction vice versa. \n
			:return: link_dirction: DLNK | ULNK Downlink/Forward Direction from BS to MS. Uplink/Backward Direction from MS to BS.
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:LDIRection?')
		return Conversions.str_to_scalar_enum(response, enums.LinkDirectionTetra)

	def set_ldirection(self, link_dirction: enums.LinkDirectionTetra) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:LDIRection \n
		Snippet: driver.configure.afRf.measurement.digital.tetra.set_ldirection(link_dirction = enums.LinkDirectionTetra.DLNK) \n
		Sets either the Downlink/forward or the uplink/backward direction of the test. The downlink direction is from BS to MS,
		the uplink direction vice versa. \n
			:param link_dirction: DLNK | ULNK Downlink/Forward Direction from BS to MS. Uplink/Backward Direction from MS to BS.
		"""
		param = Conversions.enum_scalar_to_str(link_dirction, enums.LinkDirectionTetra)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:LDIRection {param}')

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.PatternTetra:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:PATTern \n
		Snippet: value: enums.PatternTetra = driver.configure.afRf.measurement.digital.tetra.get_pattern() \n
		Selects the pattern type. \n
			:return: pattern: S1 | S2 | S3
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.PatternTetra)

	# noinspection PyTypeChecker
	def get_ber_period(self) -> enums.BerPeriod:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:BERPeriod \n
		Snippet: value: enums.BerPeriod = driver.configure.afRf.measurement.digital.tetra.get_ber_period() \n
		Sets the period, i.e. the number of frames for the bit error rate. Select 36 or 48 frames. \n
			:return: ber_period: F36 | F48 36 Frames The bit error rate is calculated from 36 frames of the bit stream. 48 Frames The bit error rate is calculated from 48 frames of the bit stream.
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:BERPeriod?')
		return Conversions.str_to_scalar_enum(response, enums.BerPeriod)

	def set_ber_period(self, ber_period: enums.BerPeriod) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:BERPeriod \n
		Snippet: driver.configure.afRf.measurement.digital.tetra.set_ber_period(ber_period = enums.BerPeriod.F36) \n
		Sets the period, i.e. the number of frames for the bit error rate. Select 36 or 48 frames. \n
			:param ber_period: F36 | F48 36 Frames The bit error rate is calculated from 36 frames of the bit stream. 48 Frames The bit error rate is calculated from 48 frames of the bit stream.
		"""
		param = Conversions.enum_scalar_to_str(ber_period, enums.BerPeriod)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:BERPeriod {param}')

	# noinspection PyTypeChecker
	def get_payload(self) -> enums.PayloadTypeTetra:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:PAYLoad \n
		Snippet: value: enums.PayloadTypeTetra = driver.configure.afRf.measurement.digital.tetra.get_payload() \n
		Defines the payload type. \n
			:return: payload_type: ALLZero | ALLO | ALTE | PRBS9 | USER All Zeros The payload contains a binary sequence of all 0. All Ones The payload contains a binary sequence of all 1. AlternatinG The payload contains a binary sequence with alternating 0 and 1. PRBS-9 The payload contains a pseudo-random binary sequence with 511 bits (29-1) . User The payload contains a user-defined binary sequence.
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:PAYLoad?')
		return Conversions.str_to_scalar_enum(response, enums.PayloadTypeTetra)

	# noinspection PyTypeChecker
	def get_ctype(self) -> enums.ChannelTypeTetra:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:CTYPe \n
		Snippet: value: enums.ChannelTypeTetra = driver.configure.afRf.measurement.digital.tetra.get_ctype() \n
		Sets the channel type. It is fixed to 0. \n
			:return: channel_type: CT0 | CT1 | CT2 | CT3 | CT4 | CT21 | CT22 | CT24
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:CTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelTypeTetra)

	def set_ctype(self, channel_type: enums.ChannelTypeTetra) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:CTYPe \n
		Snippet: driver.configure.afRf.measurement.digital.tetra.set_ctype(channel_type = enums.ChannelTypeTetra.CT0) \n
		Sets the channel type. It is fixed to 0. \n
			:param channel_type: CT0 | CT1 | CT2 | CT3 | CT4 | CT21 | CT22 | CT24
		"""
		param = Conversions.enum_scalar_to_str(channel_type, enums.ChannelTypeTetra)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:CTYPe {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.TestModeTetra:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:TMODe \n
		Snippet: value: enums.TestModeTetra = driver.configure.afRf.measurement.digital.tetra.get_tmode() \n
		Sets the test mode. The T1 test mode is fixed. \n
			:return: test_mode: VSE | T1 | SIDecoding
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.TestModeTetra)

	# noinspection PyTypeChecker
	def get_cmode(self) -> enums.ChannelModeTetra:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:CMODe \n
		Snippet: value: enums.ChannelModeTetra = driver.configure.afRf.measurement.digital.tetra.get_cmode() \n
		The TCH 7.2 traffic channel mode is preset. \n
			:return: channel_mode: TCH72
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:CMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ChannelModeTetra)

	def set_cmode(self, channel_mode: enums.ChannelModeTetra) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:CMODe \n
		Snippet: driver.configure.afRf.measurement.digital.tetra.set_cmode(channel_mode = enums.ChannelModeTetra.TCH72) \n
		The TCH 7.2 traffic channel mode is preset. \n
			:param channel_mode: TCH72
		"""
		param = Conversions.enum_scalar_to_str(channel_mode, enums.ChannelModeTetra)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:CMODe {param}')

	def get_rprbs(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:RPRBs \n
		Snippet: value: bool = driver.configure.afRf.measurement.digital.tetra.get_rprbs() \n
		Resets the PRBS bit pattern at frame 0. \n
			:return: reset_prbs_at_fm_zero: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:RPRBs?')
		return Conversions.str_to_bool(response)

	def set_rprbs(self, reset_prbs_at_fm_zero: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:RPRBs \n
		Snippet: driver.configure.afRf.measurement.digital.tetra.set_rprbs(reset_prbs_at_fm_zero = False) \n
		Resets the PRBS bit pattern at frame 0. \n
			:param reset_prbs_at_fm_zero: OFF | ON
		"""
		param = Conversions.bool_to_str(reset_prbs_at_fm_zero)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:RPRBs {param}')

	# noinspection PyTypeChecker
	def get_filter_py(self) -> enums.FilterDigital:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:FILTer \n
		Snippet: value: enums.FilterDigital = driver.configure.afRf.measurement.digital.tetra.get_filter_py() \n
		Selects the filter type for pulse shaping of TETRA. \n
			:return: filter_py: GAUSs | RRC | COSine | SINC
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:FILTer?')
		return Conversions.str_to_scalar_enum(response, enums.FilterDigital)

	def get_ro_factor(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:ROFactor \n
		Snippet: value: float = driver.configure.afRf.measurement.digital.tetra.get_ro_factor() \n
		Sets the roll-off factor of the filter used for pulse shaping of TETRA. \n
			:return: rolloff_factor: Range: 0 to 1
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:ROFactor?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Tetra':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tetra(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
