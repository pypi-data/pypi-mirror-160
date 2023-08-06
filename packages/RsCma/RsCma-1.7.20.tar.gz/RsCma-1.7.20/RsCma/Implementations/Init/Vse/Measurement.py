from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Measurement:
	"""Measurement commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("measurement", core, parent)

	def set(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INIT:VSE:MEASurement<Instance> \n
		Snippet: driver.init.vse.measurement.set() \n
		Starts or continues the measurement. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INIT:VSE:MEASurement<Instance>', opc_timeout_ms)
