from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Average:
	"""Average commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("average", core, parent)

	def get_aperture(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:AVERage:APERture \n
		Snippet: value: float = driver.configure.gprfMeasurement.extPwrSensor.average.get_aperture() \n
		Defines the size of the acquisition interval. \n
			:return: aperture: Range: 10E-6 s to 0.3 s, Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:AVERage:APERture?')
		return Conversions.str_to_float(response)

	def set_aperture(self, aperture: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:AVERage:APERture \n
		Snippet: driver.configure.gprfMeasurement.extPwrSensor.average.set_aperture(aperture = 1.0) \n
		Defines the size of the acquisition interval. \n
			:param aperture: Range: 10E-6 s to 0.3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(aperture)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:AVERage:APERture {param}')
