from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ModDepth:
	"""ModDepth commands group definition. 5 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("modDepth", core, parent)

	@property
	def trace(self):
		"""trace commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_trace'):
			from .Trace import Trace
			self._trace = Trace(self._core, self._cmd_group)
		return self._trace

	def fetch(self) -> float:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:MDEPth \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.tsensitivity.modDepth.fetch() \n
		Query the modulation depth result for the TX modulation sensitivity search routine. CALCulate commands return error
		indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: mod_depth: Modulation depth of the demodulated signal Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:MDEPth?', suppressed)
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def calculate(self) -> enums.ResultStatus:
		"""SCPI: CALCulate:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:MDEPth \n
		Snippet: value: enums.ResultStatus = driver.afRf.measurement.searchRoutines.tsensitivity.modDepth.calculate() \n
		Query the modulation depth result for the TX modulation sensitivity search routine. CALCulate commands return error
		indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: mod_depth: Modulation depth of the demodulated signal Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'CALCulate:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:MDEPth?', suppressed)
		return Conversions.str_to_scalar_enum(response, enums.ResultStatus)

	def read(self) -> float:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:MDEPth \n
		Snippet: value: float = driver.afRf.measurement.searchRoutines.tsensitivity.modDepth.read() \n
		Query the modulation depth result for the TX modulation sensitivity search routine. CALCulate commands return error
		indicators instead of measurement values. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: mod_depth: Modulation depth of the demodulated signal Unit: %"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:SROutines:TSENsitivity:MDEPth?', suppressed)
		return Conversions.str_to_float(response)

	def clone(self) -> 'ModDepth':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ModDepth(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
