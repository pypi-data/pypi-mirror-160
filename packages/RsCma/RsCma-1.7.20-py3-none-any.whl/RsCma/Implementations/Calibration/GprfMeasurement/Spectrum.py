from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spectrum:
	"""Spectrum commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spectrum", core, parent)

	def get_tgenerator(self) -> bool:
		"""SCPI: CALibration:GPRF:MEASurement<Instance>:SPECtrum:TGENerator \n
		Snippet: value: bool = driver.calibration.gprfMeasurement.spectrum.get_tgenerator() \n
		Starts or aborts the calibration for a tracking generator setup. \n
			:return: calibrate: OFF | ON ON Setting ON starts the calibration. Return value ON indicates an ongoing calibration. OFF Setting OFF aborts an ongoing calibration. Return value OFF indicates that there is no ongoing calibration.
		"""
		response = self._core.io.query_str('CALibration:GPRF:MEASurement<Instance>:SPECtrum:TGENerator?')
		return Conversions.str_to_bool(response)

	def set_tgenerator(self, calibrate: bool) -> None:
		"""SCPI: CALibration:GPRF:MEASurement<Instance>:SPECtrum:TGENerator \n
		Snippet: driver.calibration.gprfMeasurement.spectrum.set_tgenerator(calibrate = False) \n
		Starts or aborts the calibration for a tracking generator setup. \n
			:param calibrate: OFF | ON ON Setting ON starts the calibration. Return value ON indicates an ongoing calibration. OFF Setting OFF aborts an ongoing calibration. Return value OFF indicates that there is no ongoing calibration.
		"""
		param = Conversions.bool_to_str(calibrate)
		self._core.io.write(f'CALibration:GPRF:MEASurement<Instance>:SPECtrum:TGENerator {param}')
