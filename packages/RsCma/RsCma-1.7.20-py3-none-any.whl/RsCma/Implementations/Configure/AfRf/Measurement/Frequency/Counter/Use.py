from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Use:
	"""Use commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("use", core, parent)

	def set(self) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:USE \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.use.set() \n
			INTRO_CMD_HELP: Applies the search results to the RF settings: \n
			- The center frequency of the RF analyzer is set to the counted frequency.
			- The expected power is set to the measured power plus 10 dB. \n
		"""
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:USE')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:USE \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.use.set_with_opc() \n
			INTRO_CMD_HELP: Applies the search results to the RF settings: \n
			- The center frequency of the RF analyzer is set to the counted frequency.
			- The expected power is set to the measured power plus 10 dB. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:USE', opc_timeout_ms)
