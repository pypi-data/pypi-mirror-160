from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SearchRoutines:
	"""SearchRoutines commands group definition. 85 total commands, 7 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("searchRoutines", core, parent)

	@property
	def tvaDelay(self):
		"""tvaDelay commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tvaDelay'):
			from .TvaDelay import TvaDelay
			self._tvaDelay = TvaDelay(self._core, self._cmd_group)
		return self._tvaDelay

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._cmd_group)
		return self._state

	@property
	def rsensitivity(self):
		"""rsensitivity commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_rsensitivity'):
			from .Rsensitivity import Rsensitivity
			self._rsensitivity = Rsensitivity(self._core, self._cmd_group)
		return self._rsensitivity

	@property
	def rifBandwidth(self):
		"""rifBandwidth commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_rifBandwidth'):
			from .RifBandwidth import RifBandwidth
			self._rifBandwidth = RifBandwidth(self._core, self._cmd_group)
		return self._rifBandwidth

	@property
	def rsquelch(self):
		"""rsquelch commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_rsquelch'):
			from .Rsquelch import Rsquelch
			self._rsquelch = Rsquelch(self._core, self._cmd_group)
		return self._rsquelch

	@property
	def ssnr(self):
		"""ssnr commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_ssnr'):
			from .Ssnr import Ssnr
			self._ssnr = Ssnr(self._core, self._cmd_group)
		return self._ssnr

	@property
	def tsensitivity(self):
		"""tsensitivity commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsensitivity'):
			from .Tsensitivity import Tsensitivity
			self._tsensitivity = Tsensitivity(self._core, self._cmd_group)
		return self._tsensitivity

	def initiate(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INITiate:AFRF:MEASurement<Instance>:SROutines \n
		Snippet: driver.afRf.measurement.searchRoutines.initiate() \n
		Starts or continues the search routine. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INITiate:AFRF:MEASurement<Instance>:SROutines', opc_timeout_ms)

	def stop(self) -> None:
		"""SCPI: STOP:AFRF:MEASurement<Instance>:SROutines \n
		Snippet: driver.afRf.measurement.searchRoutines.stop() \n
		Pauses the search routine. \n
		"""
		self._core.io.write(f'STOP:AFRF:MEASurement<Instance>:SROutines')

	def stop_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: STOP:AFRF:MEASurement<Instance>:SROutines \n
		Snippet: driver.afRf.measurement.searchRoutines.stop_with_opc() \n
		Pauses the search routine. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'STOP:AFRF:MEASurement<Instance>:SROutines', opc_timeout_ms)

	def abort(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: ABORt:AFRF:MEASurement<Instance>:SROutines \n
		Snippet: driver.afRf.measurement.searchRoutines.abort() \n
		Stops the search routine. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'ABORt:AFRF:MEASurement<Instance>:SROutines', opc_timeout_ms)

	def clone(self) -> 'SearchRoutines':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = SearchRoutines(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
