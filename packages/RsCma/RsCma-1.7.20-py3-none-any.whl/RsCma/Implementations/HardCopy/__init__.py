from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HardCopy:
	"""HardCopy commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("hardCopy", core, parent)

	@property
	def device(self):
		"""device commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_device'):
			from .Device import Device
			self._device = Device(self._core, self._cmd_group)
		return self._device

	def get_data(self) -> bytes:
		"""SCPI: HCOPy:DATA \n
		Snippet: value: bytes = driver.hardCopy.get_data() \n
		Captures a screenshot and returns the result in block data format, see also 'Block data'. It is recommended to 'switch
		on' the display before sending this command, see method RsCma.System.Display.update. \n
			:return: data: Screenshot in 488.2 block data format
		"""
		response = self._core.io.query_bin_block('HCOPy:DATA?')
		return response

	def set_file(self, filename: str) -> None:
		"""SCPI: HCOPy:FILE \n
		Snippet: driver.hardCopy.set_file(filename = '1') \n
		Captures a screenshot and stores it to the specified file. It is recommended to 'switch on' the display before sending
		this command, see method RsCma.System.Display.update. \n
			:param filename: String parameter specifying the absolute path and name of the file. The file extension is added automatically according to the configured format (see method RsCma.HardCopy.Device.formatPy) .
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'HCOPy:FILE {param}')

	def clone(self) -> 'HardCopy':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = HardCopy(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
