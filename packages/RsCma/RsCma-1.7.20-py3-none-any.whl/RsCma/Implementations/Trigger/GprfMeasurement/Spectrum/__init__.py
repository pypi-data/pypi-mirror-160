from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spectrum:
	"""Spectrum commands group definition. 7 total commands, 1 Subgroups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spectrum", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import Catalog
			self._catalog = Catalog(self._core, self._cmd_group)
		return self._catalog

	def get_threshold(self) -> float:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:THReshold \n
		Snippet: value: float = driver.trigger.gprfMeasurement.spectrum.get_threshold() \n
		Defines the trigger threshold for trigger source 'Video'. \n
			:return: threshold: Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to expected power minus external attenuation)
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:SPECtrum:THReshold?')
		return Conversions.str_to_float(response)

	def set_threshold(self, threshold: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:THReshold \n
		Snippet: driver.trigger.gprfMeasurement.spectrum.set_threshold(threshold = 1.0) \n
		Defines the trigger threshold for trigger source 'Video'. \n
			:param threshold: Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to expected power minus external attenuation)
		"""
		param = Conversions.decimal_value_to_str(threshold)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:SPECtrum:THReshold {param}')

	def get_source(self) -> str:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:SOURce \n
		Snippet: value: str = driver.trigger.gprfMeasurement.spectrum.get_source() \n
		Selects a trigger event source for spectrum analysis. To query a list of all supported sources, use method RsCma.Trigger.
		GprfMeasurement.Spectrum.Catalog.source. \n
			:return: source: Source as string, examples: 'Free Run' Immediate start without trigger signal 'Video' Trigger by video power steps 'Base1: External TRIG In' Trigger signal at connector TRIG IN 'AFRF Gen1: ...' Trigger by processed waveform file
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:SPECtrum:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:SOURce \n
		Snippet: driver.trigger.gprfMeasurement.spectrum.set_source(source = '1') \n
		Selects a trigger event source for spectrum analysis. To query a list of all supported sources, use method RsCma.Trigger.
		GprfMeasurement.Spectrum.Catalog.source. \n
			:param source: Source as string, examples: 'Free Run' Immediate start without trigger signal 'Video' Trigger by video power steps 'Base1: External TRIG In' Trigger signal at connector TRIG IN 'AFRF Gen1: ...' Trigger by processed waveform file
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:SPECtrum:SOURce {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlopeExt:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:SLOPe \n
		Snippet: value: enums.SignalSlopeExt = driver.trigger.gprfMeasurement.spectrum.get_slope() \n
		Selects whether the trigger event is generated at the rising or at the falling edge of the trigger pulse. This command is
		relevant for the trigger source 'Video'. \n
			:return: slope: REDGe | FEDGe | RISing | FALLing REDGe, RISing Rising edge FEDGe, FALLing Falling edge
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:SPECtrum:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlopeExt)

	def set_slope(self, slope: enums.SignalSlopeExt) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:SLOPe \n
		Snippet: driver.trigger.gprfMeasurement.spectrum.set_slope(slope = enums.SignalSlopeExt.FALLing) \n
		Selects whether the trigger event is generated at the rising or at the falling edge of the trigger pulse. This command is
		relevant for the trigger source 'Video'. \n
			:param slope: REDGe | FEDGe | RISing | FALLing REDGe, RISing Rising edge FEDGe, FALLing Falling edge
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.SignalSlopeExt)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:SPECtrum:SLOPe {param}')

	def get_mgap(self) -> float:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:MGAP \n
		Snippet: value: float = driver.trigger.gprfMeasurement.spectrum.get_mgap() \n
		Defines the minimum duration of the power-down periods (gaps) between two triggered power pulses. This setting is
		relevant for trigger source 'Video'. \n
			:return: minimum_gap: Range: 0 s to 0.01 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:SPECtrum:MGAP?')
		return Conversions.str_to_float(response)

	def set_mgap(self, minimum_gap: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:MGAP \n
		Snippet: driver.trigger.gprfMeasurement.spectrum.set_mgap(minimum_gap = 1.0) \n
		Defines the minimum duration of the power-down periods (gaps) between two triggered power pulses. This setting is
		relevant for trigger source 'Video'. \n
			:param minimum_gap: Range: 0 s to 0.01 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(minimum_gap)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:SPECtrum:MGAP {param}')

	def get_offset(self) -> float:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:OFFSet \n
		Snippet: value: float = driver.trigger.gprfMeasurement.spectrum.get_offset() \n
		Defines a delay time for triggered zero span measurements. The trigger offset delays the start of the measurement
		relative to the trigger event. This command is relevant for the trigger source 'Video' and for trigger signals at TRIG IN. \n
			:return: trigger_offset: Range: -0.5 s to 0.5 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:SPECtrum:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, trigger_offset: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:OFFSet \n
		Snippet: driver.trigger.gprfMeasurement.spectrum.set_offset(trigger_offset = 1.0) \n
		Defines a delay time for triggered zero span measurements. The trigger offset delays the start of the measurement
		relative to the trigger event. This command is relevant for the trigger source 'Video' and for trigger signals at TRIG IN. \n
			:param trigger_offset: Range: -0.5 s to 0.5 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(trigger_offset)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:SPECtrum:OFFSet {param}')

	def get_timeout(self) -> float:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:TOUT \n
		Snippet: value: float = driver.trigger.gprfMeasurement.spectrum.get_timeout() \n
		Specifies the time after which an initiated measurement must have received a trigger event. If no trigger event is
		received, the measurement is stopped in remote control mode. In manual operation mode, a trigger timeout is indicated.
		This setting is relevant for the trigger source 'Video' and for trigger signals at TRIG IN. \n
			:return: trigger_timeout: Range: 0.01 s to 300 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:SPECtrum:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, trigger_timeout: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:SPECtrum:TOUT \n
		Snippet: driver.trigger.gprfMeasurement.spectrum.set_timeout(trigger_timeout = 1.0) \n
		Specifies the time after which an initiated measurement must have received a trigger event. If no trigger event is
		received, the measurement is stopped in remote control mode. In manual operation mode, a trigger timeout is indicated.
		This setting is relevant for the trigger source 'Video' and for trigger signals at TRIG IN. \n
			:param trigger_timeout: Range: 0.01 s to 300 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(trigger_timeout)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:SPECtrum:TOUT {param}')

	def clone(self) -> 'Spectrum':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Spectrum(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
