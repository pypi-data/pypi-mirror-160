from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FftSpecAn:
	"""FftSpecAn commands group definition. 9 total commands, 2 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fftSpecAn", core, parent)

	@property
	def osStop(self):
		"""osStop commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_osStop'):
			from .OsStop import OsStop
			self._osStop = OsStop(self._core, self._cmd_group)
		return self._osStop

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import Catalog
			self._catalog = Catalog(self._core, self._cmd_group)
		return self._catalog

	# noinspection PyTypeChecker
	def get_omode(self) -> enums.FftOffsetMode:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OMODe \n
		Snippet: value: enums.FftOffsetMode = driver.trigger.gprfMeasurement.fftSpecAn.get_omode() \n
		Selects the trigger offset mode. \n
			:return: offset_mode: VARiable | FIXed VARiable Variable trigger offset within a configurable range FIXed Static configurable trigger offset
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OMODe?')
		return Conversions.str_to_scalar_enum(response, enums.FftOffsetMode)

	def set_omode(self, offset_mode: enums.FftOffsetMode) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OMODe \n
		Snippet: driver.trigger.gprfMeasurement.fftSpecAn.set_omode(offset_mode = enums.FftOffsetMode.FIXed) \n
		Selects the trigger offset mode. \n
			:param offset_mode: VARiable | FIXed VARiable Variable trigger offset within a configurable range FIXed Static configurable trigger offset
		"""
		param = Conversions.enum_scalar_to_str(offset_mode, enums.FftOffsetMode)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OMODe {param}')

	def get_source(self) -> str:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:SOURce \n
		Snippet: value: str = driver.trigger.gprfMeasurement.fftSpecAn.get_source() \n
		Selects a trigger event source for FFT spectrum analysis. To query a list of all supported sources, use method RsCma.
		Trigger.GprfMeasurement.FftSpecAn.Catalog.source. \n
			:return: source: Source as string, examples: 'Free Run' Immediate start without trigger signal 'IF Power' Trigger by IF power steps 'Base1: External TRIG In' Trigger signal at connector TRIG IN 'AFRF Gen1: ...' Trigger by processed waveform file
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:SOURce \n
		Snippet: driver.trigger.gprfMeasurement.fftSpecAn.set_source(source = '1') \n
		Selects a trigger event source for FFT spectrum analysis. To query a list of all supported sources, use method RsCma.
		Trigger.GprfMeasurement.FftSpecAn.Catalog.source. \n
			:param source: Source as string, examples: 'Free Run' Immediate start without trigger signal 'IF Power' Trigger by IF power steps 'Base1: External TRIG In' Trigger signal at connector TRIG IN 'AFRF Gen1: ...' Trigger by processed waveform file
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:SOURce {param}')

	def get_mgap(self) -> float:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:MGAP \n
		Snippet: value: float = driver.trigger.gprfMeasurement.fftSpecAn.get_mgap() \n
		Defines the minimum duration of the power-down periods (gaps) between two triggered power pulses. This setting is
		relevant for the trigger source 'IF Power'. \n
			:return: minimum_gap: Range: 0 s to 0.01 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:MGAP?')
		return Conversions.str_to_float(response)

	def set_mgap(self, minimum_gap: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:MGAP \n
		Snippet: driver.trigger.gprfMeasurement.fftSpecAn.set_mgap(minimum_gap = 1.0) \n
		Defines the minimum duration of the power-down periods (gaps) between two triggered power pulses. This setting is
		relevant for the trigger source 'IF Power'. \n
			:param minimum_gap: Range: 0 s to 0.01 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(minimum_gap)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:MGAP {param}')

	def get_timeout(self) -> float or bool:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:TOUT \n
		Snippet: value: float or bool = driver.trigger.gprfMeasurement.fftSpecAn.get_timeout() \n
		Specifies the time after which an initiated measurement must have received a trigger event. If no trigger event is
		received, the measurement is stopped in remote control mode. In manual operation mode, a trigger timeout is indicated.
		This setting is relevant for the trigger source 'IF Power' and for trigger signals at TRIG IN. \n
			:return: timeout: (float or boolean) Range: 0.01 s to 300 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:TOUT?')
		return Conversions.str_to_float_or_bool(response)

	def set_timeout(self, timeout: float or bool) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:TOUT \n
		Snippet: driver.trigger.gprfMeasurement.fftSpecAn.set_timeout(timeout = 1.0) \n
		Specifies the time after which an initiated measurement must have received a trigger event. If no trigger event is
		received, the measurement is stopped in remote control mode. In manual operation mode, a trigger timeout is indicated.
		This setting is relevant for the trigger source 'IF Power' and for trigger signals at TRIG IN. \n
			:param timeout: (float or boolean) Range: 0.01 s to 300 s, Unit: s
		"""
		param = Conversions.decimal_or_bool_value_to_str(timeout)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:TOUT {param}')

	def get_offset(self) -> float:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OFFSet \n
		Snippet: value: float = driver.trigger.gprfMeasurement.fftSpecAn.get_offset() \n
		Defines a trigger offset for the FIXed trigger offset mode, see method RsCma.Trigger.GprfMeasurement.FftSpecAn.omode. \n
			:return: offset: Range: -0.15 s to 0.15 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OFFSet \n
		Snippet: driver.trigger.gprfMeasurement.fftSpecAn.set_offset(offset = 1.0) \n
		Defines a trigger offset for the FIXed trigger offset mode, see method RsCma.Trigger.GprfMeasurement.FftSpecAn.omode. \n
			:param offset: Range: -0.15 s to 0.15 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:OFFSet {param}')

	def get_threshold(self) -> float:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:THReshold \n
		Snippet: value: float = driver.trigger.gprfMeasurement.fftSpecAn.get_threshold() \n
		Defines the trigger threshold for trigger source 'IF Power'. \n
			:return: threshold: Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to expected power minus external attenuation)
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:THReshold?')
		return Conversions.str_to_float(response)

	def set_threshold(self, threshold: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:THReshold \n
		Snippet: driver.trigger.gprfMeasurement.fftSpecAn.set_threshold(threshold = 1.0) \n
		Defines the trigger threshold for trigger source 'IF Power'. \n
			:param threshold: Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to expected power minus external attenuation)
		"""
		param = Conversions.decimal_value_to_str(threshold)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:THReshold {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlopeExt:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:SLOPe \n
		Snippet: value: enums.SignalSlopeExt = driver.trigger.gprfMeasurement.fftSpecAn.get_slope() \n
		Selects whether the trigger event is generated at the rising or at the falling edge of the trigger pulse. This command is
		relevant for trigger source 'IF Power'. \n
			:return: event: REDGe | FEDGe | RISing | FALLing REDGe, RISing Rising edge FEDGe, FALLing Falling edge
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlopeExt)

	def set_slope(self, event: enums.SignalSlopeExt) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:SLOPe \n
		Snippet: driver.trigger.gprfMeasurement.fftSpecAn.set_slope(event = enums.SignalSlopeExt.FALLing) \n
		Selects whether the trigger event is generated at the rising or at the falling edge of the trigger pulse. This command is
		relevant for trigger source 'IF Power'. \n
			:param event: REDGe | FEDGe | RISing | FALLing REDGe, RISing Rising edge FEDGe, FALLing Falling edge
		"""
		param = Conversions.enum_scalar_to_str(event, enums.SignalSlopeExt)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:FFTSanalyzer:SLOPe {param}')

	def clone(self) -> 'FftSpecAn':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FftSpecAn(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
