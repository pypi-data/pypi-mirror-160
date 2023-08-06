from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Attenuation:
	"""Attenuation commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("attenuation", core, parent)

	def get_state(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation:STATe \n
		Snippet: value: bool = driver.configure.gprfMeasurement.extPwrSensor.attenuation.get_state() \n
		Specifies whether there is an attenuator or amplifier between the power sensor and the DUT. \n
			:return: attenuator_state: OFF | ON OFF Direct connection to DUT ON Attenuator or amplifier between power sensor and DUT. Configure also the attenuation, see method RsCma.Configure.GprfMeasurement.ExtPwrSensor.Attenuation.value.
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, attenuator_state: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation:STATe \n
		Snippet: driver.configure.gprfMeasurement.extPwrSensor.attenuation.set_state(attenuator_state = False) \n
		Specifies whether there is an attenuator or amplifier between the power sensor and the DUT. \n
			:param attenuator_state: OFF | ON OFF Direct connection to DUT ON Attenuator or amplifier between power sensor and DUT. Configure also the attenuation, see method RsCma.Configure.GprfMeasurement.ExtPwrSensor.Attenuation.value.
		"""
		param = Conversions.bool_to_str(attenuator_state)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation:STATe {param}')

	def get_value(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation \n
		Snippet: value: float = driver.configure.gprfMeasurement.extPwrSensor.attenuation.get_value() \n
		Specifies the attenuation or gain of a component between the power sensor and the DUT. The power readings are corrected
		accordingly. Configure also the attenuation state, see method RsCma.Configure.GprfMeasurement.ExtPwrSensor.Attenuation.
		state. \n
			:return: attenuation: Range: -50 dB to 50 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation?')
		return Conversions.str_to_float(response)

	def set_value(self, attenuation: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation \n
		Snippet: driver.configure.gprfMeasurement.extPwrSensor.attenuation.set_value(attenuation = 1.0) \n
		Specifies the attenuation or gain of a component between the power sensor and the DUT. The power readings are corrected
		accordingly. Configure also the attenuation state, see method RsCma.Configure.GprfMeasurement.ExtPwrSensor.Attenuation.
		state. \n
			:param attenuation: Range: -50 dB to 50 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(attenuation)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:EPSensor:ATTenuation {param}')
