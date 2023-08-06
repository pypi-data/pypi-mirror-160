from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vswr:
	"""Vswr commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vswr", core, parent)

	def get_mode(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:VSWR:MODE \n
		Snippet: value: bool = driver.configure.gprfMeasurement.spectrum.vswr.get_mode() \n
		Enables the 'VSWR Mode' to measure the VSWR with CMA tracking generator. \n
			:return: vswr_mode: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:VSWR:MODE?')
		return Conversions.str_to_bool(response)

	def set_mode(self, vswr_mode: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:VSWR:MODE \n
		Snippet: driver.configure.gprfMeasurement.spectrum.vswr.set_mode(vswr_mode = False) \n
		Enables the 'VSWR Mode' to measure the VSWR with CMA tracking generator. \n
			:param vswr_mode: OFF | ON
		"""
		param = Conversions.bool_to_str(vswr_mode)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:VSWR:MODE {param}')
