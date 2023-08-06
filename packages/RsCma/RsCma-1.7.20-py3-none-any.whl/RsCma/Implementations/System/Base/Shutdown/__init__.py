from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Shutdown:
	"""Shutdown commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("shutdown", core, parent)

	@property
	def device(self):
		"""device commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_device'):
			from .Device import Device
			self._device = Device(self._core, self._cmd_group)
		return self._device

	def set(self) -> None:
		"""SCPI: SYSTem:BASE:SHUTdown \n
		Snippet: driver.system.base.shutdown.set() \n
		Shuts down the test software and shows the desktop of the operating system. \n
		"""
		self._core.io.write(f'SYSTem:BASE:SHUTdown')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:BASE:SHUTdown \n
		Snippet: driver.system.base.shutdown.set_with_opc() \n
		Shuts down the test software and shows the desktop of the operating system. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:BASE:SHUTdown', opc_timeout_ms)

	def clone(self) -> 'Shutdown':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Shutdown(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
