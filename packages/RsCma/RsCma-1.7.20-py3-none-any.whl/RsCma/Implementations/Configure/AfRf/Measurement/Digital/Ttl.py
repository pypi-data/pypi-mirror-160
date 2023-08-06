from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ttl:
	"""Ttl commands group definition. 6 total commands, 0 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ttl", core, parent)

	# noinspection PyTypeChecker
	def get_pattern(self) -> enums.UserDefPattern:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:PATTern \n
		Snippet: value: enums.UserDefPattern = driver.configure.afRf.measurement.digital.ttl.get_pattern() \n
		Selects the bit pattern to be transmitted as payload. \n
			:return: pattern: PRBS6 | PRBS9
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:PATTern?')
		return Conversions.str_to_scalar_enum(response, enums.UserDefPattern)

	def set_pattern(self, pattern: enums.UserDefPattern) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:PATTern \n
		Snippet: driver.configure.afRf.measurement.digital.ttl.set_pattern(pattern = enums.UserDefPattern.PRBS6) \n
		Selects the bit pattern to be transmitted as payload. \n
			:param pattern: PRBS6 | PRBS9
		"""
		param = Conversions.enum_scalar_to_str(pattern, enums.UserDefPattern)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:PATTern {param}')

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.digital.ttl.get_enable() \n
		Enables or disables analysis of data from the TTL connector. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:ENABle \n
		Snippet: driver.configure.afRf.measurement.digital.ttl.set_enable(enable = False) \n
		Enables or disables analysis of data from the TTL connector. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:ENABle {param}')

	# noinspection PyTypeChecker
	def get_interface(self) -> enums.TtlInterface:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:INTerface \n
		Snippet: value: enums.TtlInterface = driver.configure.afRf.measurement.digital.ttl.get_interface() \n
		Sets '1-Wire' or '2-Wire' for the 'Interface' options field in the TTL path. \n
			:return: interface: WIRE1 | WIRE2
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:INTerface?')
		return Conversions.str_to_scalar_enum(response, enums.TtlInterface)

	def set_interface(self, interface: enums.TtlInterface) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:INTerface \n
		Snippet: driver.configure.afRf.measurement.digital.ttl.set_interface(interface = enums.TtlInterface.WIRE1) \n
		Sets '1-Wire' or '2-Wire' for the 'Interface' options field in the TTL path. \n
			:param interface: WIRE1 | WIRE2
		"""
		param = Conversions.enum_scalar_to_str(interface, enums.TtlInterface)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:INTerface {param}')

	# noinspection PyTypeChecker
	def get_crate(self) -> enums.ClockRate:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:CRATe \n
		Snippet: value: enums.ClockRate = driver.configure.afRf.measurement.digital.ttl.get_crate() \n
		Sets the clock rate. \n
			:return: clock_rate: BPS1200 | BPS2400 | BPS4800 | BPS9600 | BPS14400 | BPS19200 | BPS28800 | BPS38400 | BPS57600 | BPS115200
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:CRATe?')
		return Conversions.str_to_scalar_enum(response, enums.ClockRate)

	def set_crate(self, clock_rate: enums.ClockRate) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:CRATe \n
		Snippet: driver.configure.afRf.measurement.digital.ttl.set_crate(clock_rate = enums.ClockRate.BPS115200) \n
		Sets the clock rate. \n
			:param clock_rate: BPS1200 | BPS2400 | BPS4800 | BPS9600 | BPS14400 | BPS19200 | BPS28800 | BPS38400 | BPS57600 | BPS115200
		"""
		param = Conversions.enum_scalar_to_str(clock_rate, enums.ClockRate)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:CRATe {param}')

	def get_bp_factor(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:BPFactor \n
		Snippet: value: int = driver.configure.afRf.measurement.digital.ttl.get_bp_factor() \n
		Sets the factor for the 'BER Period'. The factor sets the number of bits which are a multiple of the clock rate. \n
			:return: bperiod_factor: Range: 1 to 20
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:BPFactor?')
		return Conversions.str_to_int(response)

	def set_bp_factor(self, bperiod_factor: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:BPFactor \n
		Snippet: driver.configure.afRf.measurement.digital.ttl.set_bp_factor(bperiod_factor = 1) \n
		Sets the factor for the 'BER Period'. The factor sets the number of bits which are a multiple of the clock rate. \n
			:param bperiod_factor: Range: 1 to 20
		"""
		param = Conversions.decimal_value_to_str(bperiod_factor)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:BPFactor {param}')

	def get_bp_bits(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:BPBits \n
		Snippet: value: int = driver.configure.afRf.measurement.digital.ttl.get_bp_bits() \n
		Provides the number of bits for the 'BER Period'. The number of bits is a multiple of the clock rate. Set the factor in
		the 'BER Period' input field or in the following remote command: method RsCma.Configure.AfRf.Measurement.Digital.Ttl.
		bpFactor. \n
			:return: ber_period: Range: 1200 bits to 24E+3 bits, Unit: bits
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TTL:BPBits?')
		return Conversions.str_to_int(response)
