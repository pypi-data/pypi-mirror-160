from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rf:
	"""Rf commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rf", core, parent)

	# noinspection PyTypeChecker
	def get_pemphasis(self) -> enums.PreDeEmphasis:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:FILTer:RF:PEMPhasis \n
		Snippet: value: enums.PreDeEmphasis = driver.source.afRf.generator.filterPy.rf.get_pemphasis() \n
		Configures the pre-emphasis filter. \n
			:return: preemphasis: OFF | T50 | T75 | T750 OFF Filter disabled T50, T75, T750 Time constant 50 µs / 75 µs / 750 µs
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:FILTer:RF:PEMPhasis?')
		return Conversions.str_to_scalar_enum(response, enums.PreDeEmphasis)

	def set_pemphasis(self, preemphasis: enums.PreDeEmphasis) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:FILTer:RF:PEMPhasis \n
		Snippet: driver.source.afRf.generator.filterPy.rf.set_pemphasis(preemphasis = enums.PreDeEmphasis.OFF) \n
		Configures the pre-emphasis filter. \n
			:param preemphasis: OFF | T50 | T75 | T750 OFF Filter disabled T50, T75, T750 Time constant 50 µs / 75 µs / 750 µs
		"""
		param = Conversions.enum_scalar_to_str(preemphasis, enums.PreDeEmphasis)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:FILTer:RF:PEMPhasis {param}')

	# noinspection PyTypeChecker
	def get_hpass(self) -> enums.HighpassFilter:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:FILTer:RF:HPASs \n
		Snippet: value: enums.HighpassFilter = driver.source.afRf.generator.filterPy.rf.get_hpass() \n
		Configures the highpass filter. \n
			:return: highpass_filter: OFF | F300 OFF Filter disabled F300 Cutoff frequency 300 Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:FILTer:RF:HPASs?')
		return Conversions.str_to_scalar_enum(response, enums.HighpassFilter)

	def set_hpass(self, highpass_filter: enums.HighpassFilter) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:FILTer:RF:HPASs \n
		Snippet: driver.source.afRf.generator.filterPy.rf.set_hpass(highpass_filter = enums.HighpassFilter.F300) \n
		Configures the highpass filter. \n
			:param highpass_filter: OFF | F300 OFF Filter disabled F300 Cutoff frequency 300 Hz
		"""
		param = Conversions.enum_scalar_to_str(highpass_filter, enums.HighpassFilter)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:FILTer:RF:HPASs {param}')

	# noinspection PyTypeChecker
	def get_lpass(self) -> enums.LowpassFilter:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:FILTer:RF:LPASs \n
		Snippet: value: enums.LowpassFilter = driver.source.afRf.generator.filterPy.rf.get_lpass() \n
		Configures the lowpass filter. \n
			:return: lowpass_filter: OFF | F3K | F4K | F15K OFF Filter disabled F3K, F4K, F15K Cutoff frequency 3 kHz / 4 kHz / 15 kHz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:FILTer:RF:LPASs?')
		return Conversions.str_to_scalar_enum(response, enums.LowpassFilter)

	def set_lpass(self, lowpass_filter: enums.LowpassFilter) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:FILTer:RF:LPASs \n
		Snippet: driver.source.afRf.generator.filterPy.rf.set_lpass(lowpass_filter = enums.LowpassFilter.F15K) \n
		Configures the lowpass filter. \n
			:param lowpass_filter: OFF | F3K | F4K | F15K OFF Filter disabled F3K, F4K, F15K Cutoff frequency 3 kHz / 4 kHz / 15 kHz
		"""
		param = Conversions.enum_scalar_to_str(lowpass_filter, enums.LowpassFilter)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:FILTer:RF:LPASs {param}')
