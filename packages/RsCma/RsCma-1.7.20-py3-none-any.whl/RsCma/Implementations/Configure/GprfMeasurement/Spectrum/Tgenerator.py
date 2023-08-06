from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tgenerator:
	"""Tgenerator commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tgenerator", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TGENerator:ENABle \n
		Snippet: value: bool = driver.configure.gprfMeasurement.spectrum.tgenerator.get_enable() \n
		Enables the tracking mode, so that the generator application acts as tracking generator. \n
			:return: state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TGENerator:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, state: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TGENerator:ENABle \n
		Snippet: driver.configure.gprfMeasurement.spectrum.tgenerator.set_enable(state = False) \n
		Enables the tracking mode, so that the generator application acts as tracking generator. \n
			:param state: OFF | ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TGENerator:ENABle {param}')

	def get_normalize(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TGENerator:NORMalize \n
		Snippet: value: bool = driver.configure.gprfMeasurement.spectrum.tgenerator.get_normalize() \n
		Enables the normalization of the frequency sweep results for measurements with tracking generator. \n
			:return: normalize: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TGENerator:NORMalize?')
		return Conversions.str_to_bool(response)

	def set_normalize(self, normalize: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TGENerator:NORMalize \n
		Snippet: driver.configure.gprfMeasurement.spectrum.tgenerator.set_normalize(normalize = False) \n
		Enables the normalization of the frequency sweep results for measurements with tracking generator. \n
			:param normalize: OFF | ON
		"""
		param = Conversions.bool_to_str(normalize)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:TGENerator:NORMalize {param}')
