from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Self:
	"""Self commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("self", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SYSTem:COMMunicate:GPIB[:SELF]:ENABle \n
		Snippet: value: bool = driver.system.communicate.gpib.self.get_enable() \n
		Enables or disables the GPIB interface. \n
			:return: enable: No help available
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:GPIB:SELF:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SYSTem:COMMunicate:GPIB[:SELF]:ENABle \n
		Snippet: driver.system.communicate.gpib.self.set_enable(enable = False) \n
		Enables or disables the GPIB interface. \n
			:param enable: 1 | 0 1: GPIB enabled 0: GPIB disabled
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SYSTem:COMMunicate:GPIB:SELF:ENABle {param}')

	def get_addr(self) -> int:
		"""SCPI: SYSTem:COMMunicate:GPIB[:SELF]:ADDR \n
		Snippet: value: int = driver.system.communicate.gpib.self.get_addr() \n
		Sets the primary GPIB address. \n
			:return: adress_no: GPIB address, integer number Range: 0 to 30
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:GPIB:SELF:ADDR?')
		return Conversions.str_to_int(response)

	def set_addr(self, adress_no: int) -> None:
		"""SCPI: SYSTem:COMMunicate:GPIB[:SELF]:ADDR \n
		Snippet: driver.system.communicate.gpib.self.set_addr(adress_no = 1) \n
		Sets the primary GPIB address. \n
			:param adress_no: GPIB address, integer number Range: 0 to 30
		"""
		param = Conversions.decimal_value_to_str(adress_no)
		self._core.io.write(f'SYSTem:COMMunicate:GPIB:SELF:ADDR {param}')
