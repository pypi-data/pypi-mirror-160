from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class DeviceFootprint:
	"""DeviceFootprint commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("deviceFootprint", core, parent)

	def set(self, path: str = None) -> None:
		"""SCPI: SYSTem:DFPRint \n
		Snippet: driver.system.deviceFootprint.set(path = '1') \n
		No command help available \n
			:param path: No help available
		"""
		param = ''
		if path:
			param = Conversions.value_to_quoted_str(path)
		self._core.io.write(f'SYSTem:DFPRint {param}'.strip())

	def get(self) -> bytes:
		"""SCPI: SYSTem:DFPRint \n
		Snippet: value: bytes = driver.system.deviceFootprint.get() \n
		No command help available \n
			:return: xml_device_footprint: No help available"""
		response = self._core.io.query_bin_block_ERROR(f'SYSTem:DFPRint?')
		return response
