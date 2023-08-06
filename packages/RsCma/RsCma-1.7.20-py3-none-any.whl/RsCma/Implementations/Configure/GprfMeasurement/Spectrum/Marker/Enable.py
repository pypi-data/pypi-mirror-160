from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set_all(self, enable: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:MARKer:ENABle:ALL \n
		Snippet: driver.configure.gprfMeasurement.spectrum.marker.enable.set_all(enable = False) \n
		Enables or disables all markers for the frequency sweep mode and the zero span mode. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:MARKer:ENABle:ALL {param}')
