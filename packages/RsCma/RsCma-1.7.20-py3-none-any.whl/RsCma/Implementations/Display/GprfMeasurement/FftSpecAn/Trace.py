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

	def set(self, trace_enable: bool, trace: enums.TraceB = None) -> None:
		"""SCPI: DISPlay:GPRF:MEASurement<Instance>:FFTSanalyzer:TRACe \n
		Snippet: driver.display.gprfMeasurement.fftSpecAn.trace.set(trace_enable = False, trace = enums.TraceB.AVERage) \n
		Selects which traces and diagrams are displayed on the 'FFT Spectrum' tab. \n
			:param trace_enable: OFF | ON Disables or enables the trace/diagrams selected via Trace
			:param trace: CURRent | AVERage | MAXimum | MINimum | TDOMmain Selects the trace (current, average, max, min) or diagrams (time domain) to be enabled/disabled To enable or disable all traces and diagrams, omit the parameter.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('trace_enable', trace_enable, DataType.Boolean), ArgSingle('trace', trace, DataType.Enum, enums.TraceB, is_optional=True))
		self._core.io.write(f'DISPlay:GPRF:MEASurement<Instance>:FFTSanalyzer:TRACe {param}'.rstrip())
