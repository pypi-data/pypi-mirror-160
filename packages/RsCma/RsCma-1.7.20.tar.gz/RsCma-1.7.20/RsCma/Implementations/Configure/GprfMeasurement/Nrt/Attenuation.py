from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Attenuation:
	"""Attenuation commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("attenuation", core, parent)

	# noinspection PyTypeChecker
	def get_port(self) -> enums.AttenuationPort:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation:PORT \n
		Snippet: value: enums.AttenuationPort = driver.configure.gprfMeasurement.nrt.attenuation.get_port() \n
		Selects the NRT-Z port to be used as measurement point. \n
			:return: attenuation_port: SOURce | LOAD
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation:PORT?')
		return Conversions.str_to_scalar_enum(response, enums.AttenuationPort)

	def set_port(self, attenuation_port: enums.AttenuationPort) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation:PORT \n
		Snippet: driver.configure.gprfMeasurement.nrt.attenuation.set_port(attenuation_port = enums.AttenuationPort.LOAD) \n
		Selects the NRT-Z port to be used as measurement point. \n
			:param attenuation_port: SOURce | LOAD
		"""
		param = Conversions.enum_scalar_to_str(attenuation_port, enums.AttenuationPort)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation:PORT {param}')

	def get_state(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation:STATe \n
		Snippet: value: bool = driver.configure.gprfMeasurement.nrt.attenuation.get_state() \n
		Enables or disables the compensation of the external attenuation configured via method RsCma.Configure.GprfMeasurement.
		Nrt.Attenuation.value. \n
			:return: attenuator_state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, attenuator_state: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation:STATe \n
		Snippet: driver.configure.gprfMeasurement.nrt.attenuation.set_state(attenuator_state = False) \n
		Enables or disables the compensation of the external attenuation configured via method RsCma.Configure.GprfMeasurement.
		Nrt.Attenuation.value. \n
			:param attenuator_state: OFF | ON
		"""
		param = Conversions.bool_to_str(attenuator_state)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation:STATe {param}')

	def get_value(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation \n
		Snippet: value: float = driver.configure.gprfMeasurement.nrt.attenuation.get_value() \n
		Specifies the attenuation of a component between the power sensor and the DUT, typically a cable. The power readings are
		corrected accordingly, if the correction is enabled via method RsCma.Configure.GprfMeasurement.Nrt.Attenuation.state. \n
			:return: attenuation: Range: 0 dB to 100 dB, Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation?')
		return Conversions.str_to_float(response)

	def set_value(self, attenuation: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation \n
		Snippet: driver.configure.gprfMeasurement.nrt.attenuation.set_value(attenuation = 1.0) \n
		Specifies the attenuation of a component between the power sensor and the DUT, typically a cable. The power readings are
		corrected accordingly, if the correction is enabled via method RsCma.Configure.GprfMeasurement.Nrt.Attenuation.state. \n
			:param attenuation: Range: 0 dB to 100 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(attenuation)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:ATTenuation {param}')
