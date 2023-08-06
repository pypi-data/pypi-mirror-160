from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Update:
	"""Update commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("update", core, parent)

	def set(self) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:RMS:DELTa:UPDate \n
		Snippet: driver.configure.afRf.measurement.spdif.level.rms.delta.update.set() \n
		Triggers the update of the AF level measurement reference value for SPDIF path. \n
		"""
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:RMS:DELTa:UPDate')

	def set_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:RMS:DELTa:UPDate \n
		Snippet: driver.configure.afRf.measurement.spdif.level.rms.delta.update.set_with_opc() \n
		Triggers the update of the AF level measurement reference value for SPDIF path. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:AFRF:MEASurement<Instance>:SIN:LEVel:RMS:DELTa:UPDate', opc_timeout_ms)
