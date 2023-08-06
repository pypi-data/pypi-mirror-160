from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nrt:
	"""Nrt commands group definition. 30 total commands, 3 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nrt", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._cmd_group)
		return self._state

	@property
	def forward(self):
		"""forward commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_forward'):
			from .Forward import Forward
			self._forward = Forward(self._core, self._cmd_group)
		return self._forward

	@property
	def reverse(self):
		"""reverse commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_reverse'):
			from .Reverse import Reverse
			self._reverse = Reverse(self._core, self._cmd_group)
		return self._reverse

	def initiate(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:NRT \n
		Snippet: driver.gprfMeasurement.nrt.initiate() \n
		Starts or continues the NRT-Z measurement. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INITiate:GPRF:MEASurement<Instance>:NRT', opc_timeout_ms)

	def stop(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:NRT \n
		Snippet: driver.gprfMeasurement.nrt.stop() \n
		Pauses the NRT-Z measurement. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'STOP:GPRF:MEASurement<Instance>:NRT', opc_timeout_ms)

	def abort(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:NRT \n
		Snippet: driver.gprfMeasurement.nrt.abort() \n
		Stops the NRT-Z measurement. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'ABORt:GPRF:MEASurement<Instance>:NRT', opc_timeout_ms)

	def get_idn(self) -> str:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:NRT:IDN \n
		Snippet: value: str = driver.gprfMeasurement.nrt.get_idn() \n
		Queries the identification string of the connected external power sensor. \n
			:return: idn: String parameter
		"""
		response = self._core.io.query_str('FETCh:GPRF:MEASurement<Instance>:NRT:IDN?')
		return trim_str_response(response)

	def clone(self) -> 'Nrt':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nrt(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
