from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfSettings:
	"""RfSettings commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rfSettings", core, parent)

	@property
	def connector(self):
		"""connector commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_connector'):
			from .Connector import Connector
			self._connector = Connector(self._core, self._cmd_group)
		return self._connector

	def get_frequency(self) -> float:
		"""SCPI: SOURce:XRT:GENerator<Instance>:RFSettings:FREQuency \n
		Snippet: value: float = driver.source.xrt.generator.rfSettings.get_frequency() \n
		Specifies the center frequency of the unmodulated RF carrier. \n
			:return: frequency: Range: 70 MHz to 6 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:XRT:GENerator<Instance>:RFSettings:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""SCPI: SOURce:XRT:GENerator<Instance>:RFSettings:FREQuency \n
		Snippet: driver.source.xrt.generator.rfSettings.set_frequency(frequency = 1.0) \n
		Specifies the center frequency of the unmodulated RF carrier. \n
			:param frequency: Range: 70 MHz to 6 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce:XRT:GENerator<Instance>:RFSettings:FREQuency {param}')

	def get_level(self) -> float:
		"""SCPI: SOURce:XRT:GENerator<Instance>:RFSettings:LEVel \n
		Snippet: value: float = driver.source.xrt.generator.rfSettings.get_level() \n
		Specifies the RMS level of the unmodulated RF signal. \n
			:return: level: Unit: dBm
		"""
		response = self._core.io.query_str('SOURce:XRT:GENerator<Instance>:RFSettings:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: SOURce:XRT:GENerator<Instance>:RFSettings:LEVel \n
		Snippet: driver.source.xrt.generator.rfSettings.set_level(level = 1.0) \n
		Specifies the RMS level of the unmodulated RF signal. \n
			:param level: Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:XRT:GENerator<Instance>:RFSettings:LEVel {param}')

	def get_pe_power(self) -> float:
		"""SCPI: SOURce:XRT:GENerator<Instance>:RFSettings:PEPower \n
		Snippet: value: float = driver.source.xrt.generator.rfSettings.get_pe_power() \n
		Queries the peak envelope power (PEP) . \n
			:return: pe_power: Unit: dBm
		"""
		response = self._core.io.query_str('SOURce:XRT:GENerator<Instance>:RFSettings:PEPower?')
		return Conversions.str_to_float(response)

	def set_pe_power(self, pe_power: float) -> None:
		"""SCPI: SOURce:XRT:GENerator<Instance>:RFSettings:PEPower \n
		Snippet: driver.source.xrt.generator.rfSettings.set_pe_power(pe_power = 1.0) \n
		Queries the peak envelope power (PEP) . \n
			:param pe_power: Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(pe_power)
		self._core.io.write(f'SOURce:XRT:GENerator<Instance>:RFSettings:PEPower {param}')

	def clone(self) -> 'RfSettings':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfSettings(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
