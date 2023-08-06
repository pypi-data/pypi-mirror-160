from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Bandpass:
	"""Bandpass commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("bandpass", core, parent)

	def get_bandwidth(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:FILTer:BANDpass:BWIDth \n
		Snippet: value: float = driver.configure.gprfMeasurement.power.filterPy.bandpass.get_bandwidth() \n
		Selects the bandwidth for the bandpass filter. \n
			:return: bandpass_bw: You can enter values between 1 kHz and 20 MHz. The setting is rounded to the closest of the following values: 1 / 2 / 3 / 5 / 10 / 20 / 30 / 50 / 100 / 200 / 300 / 500 kHz 1 / 1.08 / 2 / 2.7 / 3 / 4.5 / 5 / 9 / 10 / 13.5 / 18 / 20 / 40 MHz Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:POWer:FILTer:BANDpass:BWIDth?')
		return Conversions.str_to_float(response)

	def set_bandwidth(self, bandpass_bw: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:POWer:FILTer:BANDpass:BWIDth \n
		Snippet: driver.configure.gprfMeasurement.power.filterPy.bandpass.set_bandwidth(bandpass_bw = 1.0) \n
		Selects the bandwidth for the bandpass filter. \n
			:param bandpass_bw: You can enter values between 1 kHz and 20 MHz. The setting is rounded to the closest of the following values: 1 / 2 / 3 / 5 / 10 / 20 / 30 / 50 / 100 / 200 / 300 / 500 kHz 1 / 1.08 / 2 / 2.7 / 3 / 4.5 / 5 / 9 / 10 / 13.5 / 18 / 20 / 40 MHz Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(bandpass_bw)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:POWer:FILTer:BANDpass:BWIDth {param}')
