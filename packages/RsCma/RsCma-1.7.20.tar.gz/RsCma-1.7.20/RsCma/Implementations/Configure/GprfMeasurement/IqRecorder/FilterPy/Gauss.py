from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gauss:
	"""Gauss commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gauss", core, parent)

	def get_bandwidth(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:GAUSs:BWIDth \n
		Snippet: value: float = driver.configure.gprfMeasurement.iqRecorder.filterPy.gauss.get_bandwidth() \n
		Selects the bandwidth for the Gaussian filter. \n
			:return: gauss_bw: You can enter values between 1 kHz and 10 MHz. The setting is rounded to the closest of the following values: 1 kHz / 10 kHz / 100 kHz / 1 MHz / 10 MHz Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:GAUSs:BWIDth?')
		return Conversions.str_to_float(response)

	def set_bandwidth(self, gauss_bw: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:GAUSs:BWIDth \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.filterPy.gauss.set_bandwidth(gauss_bw = 1.0) \n
		Selects the bandwidth for the Gaussian filter. \n
			:param gauss_bw: You can enter values between 1 kHz and 10 MHz. The setting is rounded to the closest of the following values: 1 kHz / 10 kHz / 100 kHz / 1 MHz / 10 MHz Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(gauss_bw)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:GAUSs:BWIDth {param}')
