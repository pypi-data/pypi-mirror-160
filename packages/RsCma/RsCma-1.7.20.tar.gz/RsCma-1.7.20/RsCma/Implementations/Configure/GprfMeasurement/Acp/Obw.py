from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Obw:
	"""Obw commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("obw", core, parent)

	def get_percentage(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:OBW:PERCentage \n
		Snippet: value: float = driver.configure.gprfMeasurement.acp.obw.get_percentage() \n
		Defines the power percentage to be used for calculation of the OBW results. \n
			:return: obw_percentage: Range: 70 % to 99.9 %, Unit: ppm
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:ACP:OBW:PERCentage?')
		return Conversions.str_to_float(response)

	def set_percentage(self, obw_percentage: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:OBW:PERCentage \n
		Snippet: driver.configure.gprfMeasurement.acp.obw.set_percentage(obw_percentage = 1.0) \n
		Defines the power percentage to be used for calculation of the OBW results. \n
			:param obw_percentage: Range: 70 % to 99.9 %, Unit: ppm
		"""
		param = Conversions.decimal_value_to_str(obw_percentage)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:OBW:PERCentage {param}')
