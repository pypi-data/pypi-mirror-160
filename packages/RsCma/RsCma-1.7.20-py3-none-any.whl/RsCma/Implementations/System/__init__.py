from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class System:
	"""System commands group definition. 63 total commands, 9 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("system", core, parent)

	@property
	def base(self):
		"""base commands group. 11 Sub-classes, 4 commands."""
		if not hasattr(self, '_base'):
			from .Base import Base
			self._base = Base(self._core, self._cmd_group)
		return self._base

	@property
	def deviceFootprint(self):
		"""deviceFootprint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_deviceFootprint'):
			from .DeviceFootprint import DeviceFootprint
			self._deviceFootprint = DeviceFootprint(self._core, self._cmd_group)
		return self._deviceFootprint

	@property
	def display(self):
		"""display commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_display'):
			from .Display import Display
			self._display = Display(self._core, self._cmd_group)
		return self._display

	@property
	def error(self):
		"""error commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_error'):
			from .Error import Error
			self._error = Error(self._core, self._cmd_group)
		return self._error

	@property
	def help(self):
		"""help commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_help'):
			from .Help import Help
			self._help = Help(self._core, self._cmd_group)
		return self._help

	@property
	def update(self):
		"""update commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_update'):
			from .Update import Update
			self._update = Update(self._core, self._cmd_group)
		return self._update

	@property
	def communicate(self):
		"""communicate commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_communicate'):
			from .Communicate import Communicate
			self._communicate = Communicate(self._core, self._cmd_group)
		return self._communicate

	@property
	def option(self):
		"""option commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_option'):
			from .Option import Option
			self._option = Option(self._core, self._cmd_group)
		return self._option

	@property
	def password(self):
		"""password commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_password'):
			from .Password import Password
			self._password = Password(self._core, self._cmd_group)
		return self._password

	def preset(self) -> None:
		"""SCPI: SYSTem:PRESet \n
		Snippet: driver.system.preset() \n
		Presets or resets a selected application package in all scenarios. If <Application> is omitted, all applications are
		preset or reset. \n
		"""
		self._core.io.write(f'SYSTem:PRESet')

	def preset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:PRESet \n
		Snippet: driver.system.preset_with_opc() \n
		Presets or resets a selected application package in all scenarios. If <Application> is omitted, all applications are
		preset or reset. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:PRESet', opc_timeout_ms)

	def preset_all(self) -> None:
		"""SCPI: SYSTem:PRESet:ALL \n
		Snippet: driver.system.preset_all() \n
		Presets or resets the base settings and all applications in all scenarios. \n
		"""
		self._core.io.write(f'SYSTem:PRESet:ALL')

	def preset_all_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:PRESet:ALL \n
		Snippet: driver.system.preset_all_with_opc() \n
		Presets or resets the base settings and all applications in all scenarios. \n
		Same as preset_all, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:PRESet:ALL', opc_timeout_ms)

	def preset_base(self) -> None:
		"""SCPI: SYSTem:PRESet:BASE \n
		Snippet: driver.system.preset_base() \n
		Presets or resets only the base settings, not the applications. The method RsCma.System.presetBase and method RsCma.
		System.resetBase commands do not reset the settings for 'Start Automatically', 'Repetition' and 'Stop Condition' of the
		selftest configuration. See method RsCma.System.preset and method RsCma.System.reset. \n
		"""
		self._core.io.write(f'SYSTem:PRESet:BASE')

	def preset_base_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:PRESet:BASE \n
		Snippet: driver.system.preset_base_with_opc() \n
		Presets or resets only the base settings, not the applications. The method RsCma.System.presetBase and method RsCma.
		System.resetBase commands do not reset the settings for 'Start Automatically', 'Repetition' and 'Stop Condition' of the
		selftest configuration. See method RsCma.System.preset and method RsCma.System.reset. \n
		Same as preset_base, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:PRESet:BASE', opc_timeout_ms)

	def reset(self) -> None:
		"""SCPI: SYSTem:RESet \n
		Snippet: driver.system.reset() \n
		Presets or resets a selected application package in all scenarios. If <Application> is omitted, all applications are
		preset or reset. \n
		"""
		self._core.io.write(f'SYSTem:RESet')

	def reset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:RESet \n
		Snippet: driver.system.reset_with_opc() \n
		Presets or resets a selected application package in all scenarios. If <Application> is omitted, all applications are
		preset or reset. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:RESet', opc_timeout_ms)

	def reset_all(self) -> None:
		"""SCPI: SYSTem:RESet:ALL \n
		Snippet: driver.system.reset_all() \n
		Presets or resets the base settings and all applications in all scenarios. \n
		"""
		self._core.io.write(f'SYSTem:RESet:ALL')

	def reset_all_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:RESet:ALL \n
		Snippet: driver.system.reset_all_with_opc() \n
		Presets or resets the base settings and all applications in all scenarios. \n
		Same as reset_all, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:RESet:ALL', opc_timeout_ms)

	def reset_base(self) -> None:
		"""SCPI: SYSTem:RESet:BASE \n
		Snippet: driver.system.reset_base() \n
		Presets or resets only the base settings, not the applications. The method RsCma.System.presetBase and method RsCma.
		System.resetBase commands do not reset the settings for 'Start Automatically', 'Repetition' and 'Stop Condition' of the
		selftest configuration. See method RsCma.System.preset and method RsCma.System.reset. \n
		"""
		self._core.io.write(f'SYSTem:RESet:BASE')

	def reset_base_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:RESet:BASE \n
		Snippet: driver.system.reset_base_with_opc() \n
		Presets or resets only the base settings, not the applications. The method RsCma.System.presetBase and method RsCma.
		System.resetBase commands do not reset the settings for 'Start Automatically', 'Repetition' and 'Stop Condition' of the
		selftest configuration. See method RsCma.System.preset and method RsCma.System.reset. \n
		Same as reset_base, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:RESet:BASE', opc_timeout_ms)

	def clone(self) -> 'System':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = System(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
