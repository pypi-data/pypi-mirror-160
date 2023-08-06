from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccode:
	"""Ccode commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ccode", core, parent)

	def get_calculation(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:CCODe:CALCulation \n
		Snippet: value: bool = driver.source.afRf.generator.dpmr.ccode.get_calculation() \n
		Enables or disables the calculation of the channel code, for DPMR. \n
			:return: calculation: OFF | ON
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DPMR:CCODe:CALCulation?')
		return Conversions.str_to_bool(response)

	def set_calculation(self, calculation: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:CCODe:CALCulation \n
		Snippet: driver.source.afRf.generator.dpmr.ccode.set_calculation(calculation = False) \n
		Enables or disables the calculation of the channel code, for DPMR. \n
			:param calculation: OFF | ON
		"""
		param = Conversions.bool_to_str(calculation)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DPMR:CCODe:CALCulation {param}')

	def get_value(self) -> int:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:CCODe \n
		Snippet: value: int = driver.source.afRf.generator.dpmr.ccode.get_value() \n
		Defines the channel code to be signaled to the DUT, for DPMR. \n
			:return: ccode: Range: 0 to 63
		"""
		response = self._core.io.query_str_with_opc('SOURce:AFRF:GENerator<Instance>:DPMR:CCODe?')
		return Conversions.str_to_int(response)

	def set_value(self, ccode: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DPMR:CCODe \n
		Snippet: driver.source.afRf.generator.dpmr.ccode.set_value(ccode = 1) \n
		Defines the channel code to be signaled to the DUT, for DPMR. \n
			:param ccode: Range: 0 to 63
		"""
		param = Conversions.decimal_value_to_str(ccode)
		self._core.io.write_with_opc(f'SOURce:AFRF:GENerator<Instance>:DPMR:CCODe {param}')
