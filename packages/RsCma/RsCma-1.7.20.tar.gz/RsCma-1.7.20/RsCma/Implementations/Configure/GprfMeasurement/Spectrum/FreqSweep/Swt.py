from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Swt:
	"""Swt commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("swt", core, parent)

	def get_auto(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:SWT:AUTO \n
		Snippet: value: bool = driver.configure.gprfMeasurement.spectrum.freqSweep.swt.get_auto() \n
		Enables or disables automatic configuration of the sweep time for the frequency sweep mode. \n
			:return: sweep_time_auto: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:SWT:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, sweep_time_auto: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:SWT:AUTO \n
		Snippet: driver.configure.gprfMeasurement.spectrum.freqSweep.swt.set_auto(sweep_time_auto = False) \n
		Enables or disables automatic configuration of the sweep time for the frequency sweep mode. \n
			:param sweep_time_auto: OFF | ON
		"""
		param = Conversions.bool_to_str(sweep_time_auto)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:SWT:AUTO {param}')

	def get_value(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:SWT \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.freqSweep.swt.get_value() \n
		Specifies the sweep time for the frequency sweep mode. Setting this value is only possible if the automatic configuration
		is switched off, see method RsCma.Configure.GprfMeasurement.Spectrum.FreqSweep.Swt.auto. \n
			:return: sweep_time: Range: 3.99602E-3 s to 2000 s, Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:SWT?')
		return Conversions.str_to_float(response)

	def set_value(self, sweep_time: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:SWT \n
		Snippet: driver.configure.gprfMeasurement.spectrum.freqSweep.swt.set_value(sweep_time = 1.0) \n
		Specifies the sweep time for the frequency sweep mode. Setting this value is only possible if the automatic configuration
		is switched off, see method RsCma.Configure.GprfMeasurement.Spectrum.FreqSweep.Swt.auto. \n
			:param sweep_time: Range: 3.99602E-3 s to 2000 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(sweep_time)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FSWeep:SWT {param}')
