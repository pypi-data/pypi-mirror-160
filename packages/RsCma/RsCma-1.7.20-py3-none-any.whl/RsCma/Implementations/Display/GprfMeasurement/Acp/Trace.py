from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trace:
	"""Trace commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("trace", core, parent)

	def set(self, trace_enable: bool, trace: enums.TraceC) -> None:
		"""SCPI: DISPlay:GPRF:MEASurement<Instance>:ACP:TRACe \n
		Snippet: driver.display.gprfMeasurement.acp.trace.set(trace_enable = False, trace = enums.TraceC.AVERage) \n
		Selects which set of results is displayed on the 'ACP' tab. Only one set of results is displayed at a time. Enabling one
		set disables the others. \n
			:param trace_enable: OFF | ON Disables or enables the set selected via Trace
			:param trace: CURRent | AVERage | MAXimum Selects the set of results to be enabled/disabled
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('trace_enable', trace_enable, DataType.Boolean), ArgSingle('trace', trace, DataType.Enum, enums.TraceC))
		self._core.io.write(f'DISPlay:GPRF:MEASurement<Instance>:ACP:TRACe {param}'.rstrip())
