from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rbw:
	"""Rbw commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rbw", core, parent)

	def get_auto(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:RBW:AUTO \n
		Snippet: value: bool = driver.configure.gprfMeasurement.spectrum.freqSweep.rbw.get_auto() \n
		Enables or disables automatic configuration of the resolution bandwidth (RBW) for the frequency sweep mode. \n
			:return: rbw_auto: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:RBW:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, rbw_auto: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:RBW:AUTO \n
		Snippet: driver.configure.gprfMeasurement.spectrum.freqSweep.rbw.set_auto(rbw_auto = False) \n
		Enables or disables automatic configuration of the resolution bandwidth (RBW) for the frequency sweep mode. \n
			:param rbw_auto: OFF | ON
		"""
		param = Conversions.bool_to_str(rbw_auto)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:RBW:AUTO {param}')

	def get_value(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:RBW \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.freqSweep.rbw.get_value() \n
		Selects the bandwidth of the Gaussian resolution filter for the frequency sweep mode. Setting this value is only possible
		if the automatic RBW selection is switched off, see method RsCma.Configure.GprfMeasurement.Spectrum.FreqSweep.Rbw.auto. \n
			:return: rbw: You can enter values between 100 Hz and 10 MHz. The setting is rounded to the closest of the following values: 100 / 200 / 300 / 500 Hz 1 / 2 / 3 / 5 / 10 / 20 / 30 / 50 / 100 / 200 / 300 / 500 kHz 1 / 2 / 3 / 5 / 10 MHz Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:RBW?')
		return Conversions.str_to_float(response)

	def set_value(self, rbw: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:RBW \n
		Snippet: driver.configure.gprfMeasurement.spectrum.freqSweep.rbw.set_value(rbw = 1.0) \n
		Selects the bandwidth of the Gaussian resolution filter for the frequency sweep mode. Setting this value is only possible
		if the automatic RBW selection is switched off, see method RsCma.Configure.GprfMeasurement.Spectrum.FreqSweep.Rbw.auto. \n
			:param rbw: You can enter values between 100 Hz and 10 MHz. The setting is rounded to the closest of the following values: 100 / 200 / 300 / 500 Hz 1 / 2 / 3 / 5 / 10 / 20 / 30 / 50 / 100 / 200 / 300 / 500 kHz 1 / 2 / 3 / 5 / 10 MHz Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(rbw)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:RBW {param}')
