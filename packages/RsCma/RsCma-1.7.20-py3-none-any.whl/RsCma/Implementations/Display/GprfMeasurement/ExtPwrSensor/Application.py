from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Application:
	"""Application commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("application", core, parent)

	# noinspection PyTypeChecker
	def get_select(self) -> enums.ExtPwrSensorApp:
		"""SCPI: DISPlay:GPRF:MEASurement<Instance>:EPSensor:APPLication:SELect \n
		Snippet: value: enums.ExtPwrSensorApp = driver.display.gprfMeasurement.extPwrSensor.application.get_select() \n
		Configures the display of the 'Sensor' tab. \n
			:return: application: EPS | NRTZ Show 'EPS' subtab or 'NRT-Z' subtab
		"""
		response = self._core.io.query_str('DISPlay:GPRF:MEASurement<Instance>:EPSensor:APPLication:SELect?')
		return Conversions.str_to_scalar_enum(response, enums.ExtPwrSensorApp)

	def set_select(self, application: enums.ExtPwrSensorApp) -> None:
		"""SCPI: DISPlay:GPRF:MEASurement<Instance>:EPSensor:APPLication:SELect \n
		Snippet: driver.display.gprfMeasurement.extPwrSensor.application.set_select(application = enums.ExtPwrSensorApp.EPS) \n
		Configures the display of the 'Sensor' tab. \n
			:param application: EPS | NRTZ Show 'EPS' subtab or 'NRT-Z' subtab
		"""
		param = Conversions.enum_scalar_to_str(application, enums.ExtPwrSensorApp)
		self._core.io.write(f'DISPlay:GPRF:MEASurement<Instance>:EPSensor:APPLication:SELect {param}')
