from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class OsStop:
	"""OsStop commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("osStop", core, parent)

	def set(self, offset_start: float, offset_stop: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OSSTop \n
		Snippet: driver.trigger.gprfMeasurement.fftSpecAn.osStop.set(offset_start = 1.0, offset_stop = 1.0) \n
		Defines the initial and final trigger offset for the VARiable trigger offset mode, see method RsCma.Trigger.
		GprfMeasurement.FftSpecAn.omode. \n
			:param offset_start: Range: -0.15 s to OffsetStop, Unit: s
			:param offset_stop: Range: OffsetStart to 0.15 s, Unit: s
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('offset_start', offset_start, DataType.Float), ArgSingle('offset_stop', offset_stop, DataType.Float))
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OSSTop {param}'.rstrip())

	# noinspection PyTypeChecker
	class OsStopStruct(StructBase):
		"""Response structure. Fields: \n
			- Offset_Start: float: Range: -0.15 s to OffsetStop, Unit: s
			- Offset_Stop: float: Range: OffsetStart to 0.15 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_float('Offset_Start'),
			ArgStruct.scalar_float('Offset_Stop')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Offset_Start: float = None
			self.Offset_Stop: float = None

	def get(self) -> OsStopStruct:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OSSTop \n
		Snippet: value: OsStopStruct = driver.trigger.gprfMeasurement.fftSpecAn.osStop.get() \n
		Defines the initial and final trigger offset for the VARiable trigger offset mode, see method RsCma.Trigger.
		GprfMeasurement.FftSpecAn.omode. \n
			:return: structure: for return value, see the help for OsStopStruct structure arguments."""
		return self._core.io.query_struct(f'TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OSSTop?', self.__class__.OsStopStruct())
