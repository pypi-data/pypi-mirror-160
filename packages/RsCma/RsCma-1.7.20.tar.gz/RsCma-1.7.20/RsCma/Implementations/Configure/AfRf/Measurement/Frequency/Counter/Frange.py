from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frange:
	"""Frange commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frange", core, parent)

	def get_stop(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:STOP \n
		Snippet: value: float = driver.configure.afRf.measurement.frequency.counter.frange.get_stop() \n
		Defines the maximum frequency for the search procedure. \n
			:return: upper: Range: 0 Hz to 3 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:STOP?')
		return Conversions.str_to_float(response)

	def set_stop(self, upper: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:STOP \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.frange.set_stop(upper = 1.0) \n
		Defines the maximum frequency for the search procedure. \n
			:param upper: Range: 0 Hz to 3 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(upper)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:STOP {param}')

	def get_start(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:STARt \n
		Snippet: value: float = driver.configure.afRf.measurement.frequency.counter.frange.get_start() \n
		Defines the minimum frequency for the search procedure. \n
			:return: lower: Range: 0 Hz to 3 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:STARt?')
		return Conversions.str_to_float(response)

	def set_start(self, lower: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:STARt \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.frange.set_start(lower = 1.0) \n
		Defines the minimum frequency for the search procedure. \n
			:param lower: Range: 0 Hz to 3 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(lower)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:STARt {param}')

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.frequency.counter.frange.get_enable() \n
		Selects the frequency range to be searched. \n
			:return: to_limit: OFF | ON OFF Entire supported frequency range ON Frequency range defined by the commands method RsCma.Configure.AfRf.Measurement.Frequency.Counter.Frange.start and method RsCma.Configure.AfRf.Measurement.Frequency.Counter.Frange.stop
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, to_limit: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:ENABle \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.frange.set_enable(to_limit = False) \n
		Selects the frequency range to be searched. \n
			:param to_limit: OFF | ON OFF Entire supported frequency range ON Frequency range defined by the commands method RsCma.Configure.AfRf.Measurement.Frequency.Counter.Frange.start and method RsCma.Configure.AfRf.Measurement.Frequency.Counter.Frange.stop
		"""
		param = Conversions.bool_to_str(to_limit)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FRANge:ENABle {param}')
