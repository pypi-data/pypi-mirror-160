from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gotsystem:
	"""Gotsystem commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gotsystem", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:BASE:GOTSystem \n
		Snippet: driver.system.base.gotsystem.set() \n
		Minimizes the test software and shows the desktop of the operating system. \n
		"""
		self._core.io.write(f'SYSTem:BASE:GOTSystem')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: SYSTem:BASE:GOTSystem \n
		Snippet: driver.system.base.gotsystem.set_with_opc() \n
		Minimizes the test software and shows the desktop of the operating system. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'SYSTem:BASE:GOTSystem', opc_timeout_ms)
