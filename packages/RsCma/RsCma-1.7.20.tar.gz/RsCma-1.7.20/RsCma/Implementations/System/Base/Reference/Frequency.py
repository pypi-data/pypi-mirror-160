from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.RefFreqSource:
		"""SCPI: SYSTem:BASE:REFerence:FREQuency:SOURce \n
		Snippet: value: enums.RefFreqSource = driver.system.base.reference.frequency.get_source() \n
		Selects whether an internal or external reference frequency source is used. \n
			:return: source: INTernal | EXTernal
		"""
		response = self._core.io.query_str_with_opc('SYSTem:BASE:REFerence:FREQuency:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.RefFreqSource)

	def set_source(self, source: enums.RefFreqSource) -> None:
		"""SCPI: SYSTem:BASE:REFerence:FREQuency:SOURce \n
		Snippet: driver.system.base.reference.frequency.set_source(source = enums.RefFreqSource.EXTernal) \n
		Selects whether an internal or external reference frequency source is used. \n
			:param source: INTernal | EXTernal
		"""
		param = Conversions.enum_scalar_to_str(source, enums.RefFreqSource)
		self._core.io.write_with_opc(f'SYSTem:BASE:REFerence:FREQuency:SOURce {param}')
