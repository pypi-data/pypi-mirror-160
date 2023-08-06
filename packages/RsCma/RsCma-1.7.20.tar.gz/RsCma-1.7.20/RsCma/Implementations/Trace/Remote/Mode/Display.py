from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("display", core, parent)

	def clear(self) -> None:
		"""SCPI: TRACe:REMote:MODE:DISPlay:CLEar \n
		Snippet: driver.trace.remote.mode.display.clear() \n
		Clears the display of the SCPI remote trace in analysis mode. \n
		"""
		self._core.io.write(f'TRACe:REMote:MODE:DISPlay:CLEar')

	def clear_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: TRACe:REMote:MODE:DISPlay:CLEar \n
		Snippet: driver.trace.remote.mode.display.clear_with_opc() \n
		Clears the display of the SCPI remote trace in analysis mode. \n
		Same as clear, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'TRACe:REMote:MODE:DISPlay:CLEar', opc_timeout_ms)
