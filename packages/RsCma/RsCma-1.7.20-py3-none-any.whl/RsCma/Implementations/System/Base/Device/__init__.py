from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Device:
	"""Device commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("device", core, parent)

	@property
	def license(self):
		"""license commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_license'):
			from .License import License
			self._license = License(self._core, self._cmd_group)
		return self._license

	@property
	def setup(self):
		"""setup commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_setup'):
			from .Setup import Setup
			self._setup = Setup(self._core, self._cmd_group)
		return self._setup

	def get_id(self) -> str:
		"""SCPI: SYSTem:BASE:DEVice:ID \n
		Snippet: value: str = driver.system.base.device.get_id() \n
		No command help available \n
			:return: device_id: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DEVice:ID?')
		return trim_str_response(response)

	def clone(self) -> 'Device':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Device(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
