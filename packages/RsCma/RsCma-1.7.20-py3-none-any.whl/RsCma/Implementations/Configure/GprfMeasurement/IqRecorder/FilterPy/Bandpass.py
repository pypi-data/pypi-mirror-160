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
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth \n
		Snippet: value: float = driver.configure.gprfMeasurement.iqRecorder.filterPy.bandpass.get_bandwidth() \n
		Selects the bandwidth for the bandpass filter. \n
			:return: bandpass_bw: You can enter values between 1 kHz and 40 MHz. The setting is rounded to the closest of the following values: 1 kHz / 10 kHz / 100 kHz / 1 MHz / 10 MHz / 40 MHz Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth?')
		return Conversions.str_to_float(response)

	def set_bandwidth(self, bandpass_bw: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.filterPy.bandpass.set_bandwidth(bandpass_bw = 1.0) \n
		Selects the bandwidth for the bandpass filter. \n
			:param bandpass_bw: You can enter values between 1 kHz and 40 MHz. The setting is rounded to the closest of the following values: 1 kHz / 10 kHz / 100 kHz / 1 MHz / 10 MHz / 40 MHz Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(bandpass_bw)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:BANDpass:BWIDth {param}')
