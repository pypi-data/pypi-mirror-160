from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pocsag:
	"""Pocsag commands group definition. 8 total commands, 0 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pocsag", core, parent)

	def get_standard_dev(self) -> List[float]:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:SDEViation \n
		Snippet: value: List[float] = driver.source.afRf.generator.pocsag.get_standard_dev() \n
		Configures the frequency deviations used for 2FSK modulation, for POCSAG. The values apply if inverted modulation is
		disabled. A query returns <DeviationS0>, <DeviationS1>. \n
			:return: sdeviation: No help available
		"""
		response = self._core.io.query_bin_or_ascii_float_list_with_opc('SOURce:AFRF:GENerator<Instance>:POCSag:SDEViation?')
		return response

	def set_standard_dev(self, sdeviation: List[float]) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:SDEViation \n
		Snippet: driver.source.afRf.generator.pocsag.set_standard_dev(sdeviation = [1.1, 2.2, 3.3]) \n
		Configures the frequency deviations used for 2FSK modulation, for POCSAG. The values apply if inverted modulation is
		disabled. A query returns <DeviationS0>, <DeviationS1>. \n
			:param sdeviation: No help available
		"""
		param = Conversions.list_to_csv_str(sdeviation)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:POCSag:SDEViation {param}')

	def get_imodulation(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:IMODulation \n
		Snippet: value: bool = driver.source.afRf.generator.pocsag.get_imodulation() \n
		Enables inverted modulation (symbol 0 negative deviation, symbol 1 positive deviation) , for POCSAG. \n
			:return: imod: OFF | ON
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:POCSag:IMODulation?')
		return Conversions.str_to_bool(response)

	def set_imodulation(self, imod: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:IMODulation \n
		Snippet: driver.source.afRf.generator.pocsag.set_imodulation(imod = False) \n
		Enables inverted modulation (symbol 0 negative deviation, symbol 1 positive deviation) , for POCSAG. \n
			:param imod: OFF | ON
		"""
		param = Conversions.bool_to_str(imod)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:POCSag:IMODulation {param}')

	def get_symbol_rate(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:SRATe \n
		Snippet: value: int = driver.source.afRf.generator.pocsag.get_symbol_rate() \n
		Configures the symbol rate for POCSAG. \n
			:return: srate: Range: 0 symbol/s to 5000 symbol/s, Unit: symbol/s
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:POCSag:SRATe?')
		return Conversions.str_to_int(response)

	def set_symbol_rate(self, srate: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:SRATe \n
		Snippet: driver.source.afRf.generator.pocsag.set_symbol_rate(srate = 1) \n
		Configures the symbol rate for POCSAG. \n
			:param srate: Range: 0 symbol/s to 5000 symbol/s, Unit: symbol/s
		"""
		param = Conversions.decimal_value_to_str(srate)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:POCSag:SRATe {param}')

	def get_paddress(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:PADDress \n
		Snippet: value: int = driver.source.afRf.generator.pocsag.get_paddress() \n
		Configures the pager address to which a POCSAG transmission is sent. \n
			:return: paddress: Range: 0 to 2097151
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:POCSag:PADDress?')
		return Conversions.str_to_int(response)

	def set_paddress(self, paddress: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:PADDress \n
		Snippet: driver.source.afRf.generator.pocsag.set_paddress(paddress = 1) \n
		Configures the pager address to which a POCSAG transmission is sent. \n
			:param paddress: Range: 0 to 2097151
		"""
		param = Conversions.decimal_value_to_str(paddress)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:POCSag:PADDress {param}')

	def get_fbits(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:FBITs \n
		Snippet: value: str = driver.source.afRf.generator.pocsag.get_fbits() \n
		Configures the function bits for POCSAG. \n
			:return: fbits: Range: #B0 to #B11
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:POCSag:FBITs?')
		return trim_str_response(response)

	def set_fbits(self, fbits: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:FBITs \n
		Snippet: driver.source.afRf.generator.pocsag.set_fbits(fbits = r1) \n
		Configures the function bits for POCSAG. \n
			:param fbits: Range: #B0 to #B11
		"""
		param = Conversions.value_to_str(fbits)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:POCSag:FBITs {param}')

	# noinspection PyTypeChecker
	def get_ptype(self) -> enums.PagerType:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:PTYPe \n
		Snippet: value: enums.PagerType = driver.source.afRf.generator.pocsag.get_ptype() \n
		Specifies whether a message is transmitted to the DUT and which message format is used, for POCSAG. \n
			:return: pager_type: NUMeric | ALPHanumeric | TONLy NUMeric: message in numeric format ALPHanumeric: message in alpha-numeric format TONLy: no message
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:POCSag:PTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.PagerType)

	def set_ptype(self, pager_type: enums.PagerType) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:PTYPe \n
		Snippet: driver.source.afRf.generator.pocsag.set_ptype(pager_type = enums.PagerType.ALPHanumeric) \n
		Specifies whether a message is transmitted to the DUT and which message format is used, for POCSAG. \n
			:param pager_type: NUMeric | ALPHanumeric | TONLy NUMeric: message in numeric format ALPHanumeric: message in alpha-numeric format TONLy: no message
		"""
		param = Conversions.enum_scalar_to_str(pager_type, enums.PagerType)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:POCSag:PTYPe {param}')

	def get_message(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:MESSage \n
		Snippet: value: str = driver.source.afRf.generator.pocsag.get_message() \n
		Specifies a character sequence for numeric and alphanumeric messages, for POCSAG. \n
			:return: content: Message as string
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:POCSag:MESSage?')
		return trim_str_response(response)

	def set_message(self, content: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:MESSage \n
		Snippet: driver.source.afRf.generator.pocsag.set_message(content = '1') \n
		Specifies a character sequence for numeric and alphanumeric messages, for POCSAG. \n
			:param content: Message as string
		"""
		param = Conversions.value_to_quoted_str(content)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:POCSag:MESSage {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.FskMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:POCSag:MODE \n
		Snippet: value: enums.FskMode = driver.source.afRf.generator.pocsag.get_mode() \n
		Queries the modulation type used for POCSAG. \n
			:return: mode: FSK2
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:POCSag:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.FskMode)
