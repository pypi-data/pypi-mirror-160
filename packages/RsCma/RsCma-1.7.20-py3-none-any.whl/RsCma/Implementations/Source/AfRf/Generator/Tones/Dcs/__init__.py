from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dcs:
	"""Dcs commands group definition. 8 total commands, 2 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dcs", core, parent)

	@property
	def ifsk(self):
		"""ifsk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ifsk'):
			from .Ifsk import Ifsk
			self._ifsk = Ifsk(self._core, self._cmd_group)
		return self._ifsk

	@property
	def toCode(self):
		"""toCode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_toCode'):
			from .ToCode import ToCode
			self._toCode = ToCode(self._core, self._cmd_group)
		return self._toCode

	def get_cword(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:CWORd \n
		Snippet: value: str = driver.source.afRf.generator.tones.dcs.get_cword() \n
		Specifies the DCS code number. \n
			:return: sequence: DCS code number as octal number Not allowed octal numbers are automatically rounded to the closest allowed value. Range: #Q20 to #Q777
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:DCS:CWORd?')
		return trim_str_response(response)

	def set_cword(self, sequence: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:CWORd \n
		Snippet: driver.source.afRf.generator.tones.dcs.set_cword(sequence = r1) \n
		Specifies the DCS code number. \n
			:param sequence: DCS code number as octal number Not allowed octal numbers are automatically rounded to the closest allowed value. Range: #Q20 to #Q777
		"""
		param = Conversions.value_to_str(sequence)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:DCS:CWORd {param}')

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.tones.dcs.get_enable() \n
		Enables or disables the DCS signal. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:DCS:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:ENABle \n
		Snippet: driver.source.afRf.generator.tones.dcs.set_enable(enable = False) \n
		Enables or disables the DCS signal. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:DCS:ENABle {param}')

	def get_fsk_deviation(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:FSKDeviation \n
		Snippet: value: float = driver.source.afRf.generator.tones.dcs.get_fsk_deviation() \n
		Specifies the frequency deviation used for FSK modulation of the carrier with the DCS bit stream. \n
			:return: fsk_dev: Range: 0 Hz to 10 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:DCS:FSKDeviation?')
		return Conversions.str_to_float(response)

	def set_fsk_deviation(self, fsk_dev: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:FSKDeviation \n
		Snippet: driver.source.afRf.generator.tones.dcs.set_fsk_deviation(fsk_dev = 1.0) \n
		Specifies the frequency deviation used for FSK modulation of the carrier with the DCS bit stream. \n
			:param fsk_dev: Range: 0 Hz to 10 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(fsk_dev)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:DCS:FSKDeviation {param}')

	def get_drate(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:DRATe \n
		Snippet: value: float = driver.source.afRf.generator.tones.dcs.get_drate() \n
		Queries the data rate used for DCS bit stream transmission. \n
			:return: bitrate: Range: 104.4 bit/s to 164.4 bit/s, Unit: bit/s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:DCS:DRATe?')
		return Conversions.str_to_float(response)

	def get_dr_offset(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:DROFfset \n
		Snippet: value: float = driver.source.afRf.generator.tones.dcs.get_dr_offset() \n
		Modifies the used data rate by defining an offset relative to the nominal data rate of 134.4 Bit/s. \n
			:return: roffset: Range: -30 bit/s to 30 bit/s, Unit: bit/s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:DCS:DROFfset?')
		return Conversions.str_to_float(response)

	def set_dr_offset(self, roffset: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:DROFfset \n
		Snippet: driver.source.afRf.generator.tones.dcs.set_dr_offset(roffset = 1.0) \n
		Modifies the used data rate by defining an offset relative to the nominal data rate of 134.4 Bit/s. \n
			:param roffset: Range: -30 bit/s to 30 bit/s, Unit: bit/s
		"""
		param = Conversions.decimal_value_to_str(roffset)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:DCS:DROFfset {param}')

	def get_toc_length(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:TOCLength \n
		Snippet: value: float = driver.source.afRf.generator.tones.dcs.get_toc_length() \n
		Specifies the duration of turn-off code transmissions. \n
			:return: off_length: Range: 0 s to 1 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:TONes:DCS:TOCLength?')
		return Conversions.str_to_float(response)

	def set_toc_length(self, off_length: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:TONes:DCS:TOCLength \n
		Snippet: driver.source.afRf.generator.tones.dcs.set_toc_length(off_length = 1.0) \n
		Specifies the duration of turn-off code transmissions. \n
			:param off_length: Range: 0 s to 1 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(off_length)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:TONes:DCS:TOCLength {param}')

	def clone(self) -> 'Dcs':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dcs(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
