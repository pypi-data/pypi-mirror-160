from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("result", core, parent)

	def get_ediagram(self) -> bool:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:RESult:EDIagram \n
		Snippet: value: bool = driver.configure.vse.measurement.result.get_ediagram() \n
		Enables or disables the measurement of the eye diagram. \n
			:return: eye_diagram_enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:RESult:EDIagram?')
		return Conversions.str_to_bool(response)

	def set_ediagram(self, eye_diagram_enable: bool) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:RESult:EDIagram \n
		Snippet: driver.configure.vse.measurement.result.set_ediagram(eye_diagram_enable = False) \n
		Enables or disables the measurement of the eye diagram. \n
			:param eye_diagram_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(eye_diagram_enable)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:RESult:EDIagram {param}')

	def get_power_vs_time(self) -> bool:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:RESult:PVTime \n
		Snippet: value: bool = driver.configure.vse.measurement.result.get_power_vs_time() \n
		Enables or disables the measurement of the power vs. time results. \n
			:return: power_vs_time_enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:RESult:PVTime?')
		return Conversions.str_to_bool(response)

	def set_power_vs_time(self, power_vs_time_enable: bool) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:RESult:PVTime \n
		Snippet: driver.configure.vse.measurement.result.set_power_vs_time(power_vs_time_enable = False) \n
		Enables or disables the measurement of the power vs. time results. \n
			:param power_vs_time_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(power_vs_time_enable)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:RESult:PVTime {param}')

	def get_cons(self) -> bool:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:RESult:CONS \n
		Snippet: value: bool = driver.configure.vse.measurement.result.get_cons() \n
		Enables or disables the measurement of the constellation diagram. \n
			:return: constellation_enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:RESult:CONS?')
		return Conversions.str_to_bool(response)

	def set_cons(self, constellation_enable: bool) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:RESult:CONS \n
		Snippet: driver.configure.vse.measurement.result.set_cons(constellation_enable = False) \n
		Enables or disables the measurement of the constellation diagram. \n
			:param constellation_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(constellation_enable)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:RESult:CONS {param}')

	def get_sdis(self) -> bool:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:RESult:SDIS \n
		Snippet: value: bool = driver.configure.vse.measurement.result.get_sdis() \n
		Enables or disables the measurement of the symbol distribution results. \n
			:return: sdistribution_enable: No help available
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:RESult:SDIS?')
		return Conversions.str_to_bool(response)

	def set_sdis(self, sdistribution_enable: bool) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:RESult:SDIS \n
		Snippet: driver.configure.vse.measurement.result.set_sdis(sdistribution_enable = False) \n
		Enables or disables the measurement of the symbol distribution results. \n
			:param sdistribution_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(sdistribution_enable)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:RESult:SDIS {param}')
