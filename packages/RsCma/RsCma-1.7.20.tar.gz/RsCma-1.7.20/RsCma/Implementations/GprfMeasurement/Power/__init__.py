from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 27 total commands, 8 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._cmd_group)
		return self._state

	@property
	def elapsedStats(self):
		"""elapsedStats commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_elapsedStats'):
			from .ElapsedStats import ElapsedStats
			self._elapsedStats = ElapsedStats(self._core, self._cmd_group)
		return self._elapsedStats

	@property
	def current(self):
		"""current commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_current'):
			from .Current import Current
			self._current = Current(self._core, self._cmd_group)
		return self._current

	@property
	def minimum(self):
		"""minimum commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_minimum'):
			from .Minimum import Minimum
			self._minimum = Minimum(self._core, self._cmd_group)
		return self._minimum

	@property
	def maximum(self):
		"""maximum commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_maximum'):
			from .Maximum import Maximum
			self._maximum = Maximum(self._core, self._cmd_group)
		return self._maximum

	@property
	def average(self):
		"""average commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_average'):
			from .Average import Average
			self._average = Average(self._core, self._cmd_group)
		return self._average

	@property
	def peak(self):
		"""peak commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_peak'):
			from .Peak import Peak
			self._peak = Peak(self._core, self._cmd_group)
		return self._peak

	@property
	def standardDev(self):
		"""standardDev commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_standardDev'):
			from .StandardDev import StandardDev
			self._standardDev = StandardDev(self._core, self._cmd_group)
		return self._standardDev

	def initiate(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:POWer \n
		Snippet: driver.gprfMeasurement.power.initiate() \n
		Starts or continues the power measurement. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'INITiate:GPRF:MEASurement<Instance>:POWer', opc_timeout_ms)

	def stop(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:POWer \n
		Snippet: driver.gprfMeasurement.power.stop() \n
		Pauses the power measurement. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'STOP:GPRF:MEASurement<Instance>:POWer', opc_timeout_ms)

	def abort(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:POWer \n
		Snippet: driver.gprfMeasurement.power.abort() \n
		Stops the power measurement. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'ABORt:GPRF:MEASurement<Instance>:POWer', opc_timeout_ms)

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
