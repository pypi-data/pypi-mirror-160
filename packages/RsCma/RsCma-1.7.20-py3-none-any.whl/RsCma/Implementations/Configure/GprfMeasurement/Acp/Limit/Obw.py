from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Obw:
	"""Obw commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("obw", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:OBW:ENABle \n
		Snippet: value: bool = driver.configure.gprfMeasurement.acp.limit.obw.get_enable() \n
		Enables or disables the OBW limit checks. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:OBW:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:OBW:ENABle \n
		Snippet: driver.configure.gprfMeasurement.acp.limit.obw.set_enable(enable = False) \n
		Enables or disables the OBW limit checks. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:OBW:ENABle {param}')

	def get_value(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:OBW \n
		Snippet: value: float = driver.configure.gprfMeasurement.acp.limit.obw.get_value() \n
		Configures an upper OBW limit. \n
			:return: limit: Range: 0 Hz to 8 MHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:OBW?')
		return Conversions.str_to_float(response)

	def set_value(self, limit: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:OBW \n
		Snippet: driver.configure.gprfMeasurement.acp.limit.obw.set_value(limit = 1.0) \n
		Configures an upper OBW limit. \n
			:param limit: Range: 0 Hz to 8 MHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(limit)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:OBW {param}')
