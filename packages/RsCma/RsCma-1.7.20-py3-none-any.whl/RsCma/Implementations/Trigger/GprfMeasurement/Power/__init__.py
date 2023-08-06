from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 8 total commands, 1 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import Catalog
			self._catalog = Catalog(self._core, self._cmd_group)
		return self._catalog

	def get_source(self) -> str:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:SOURce \n
		Snippet: value: str = driver.trigger.gprfMeasurement.power.get_source() \n
		Selects a trigger event source for power measurements. To query a list of all supported sources, use method RsCma.Trigger.
		GprfMeasurement.Power.Catalog.source. \n
			:return: source: Source as string, examples: 'Free Run' Immediate start without trigger signal 'IF Power' Trigger by IF power steps 'Base1: External TRIG In' Trigger signal at connector TRIG IN 'AFRF Gen1: ...' Trigger by processed waveform file
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:POWer:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:SOURce \n
		Snippet: driver.trigger.gprfMeasurement.power.set_source(source = '1') \n
		Selects a trigger event source for power measurements. To query a list of all supported sources, use method RsCma.Trigger.
		GprfMeasurement.Power.Catalog.source. \n
			:param source: Source as string, examples: 'Free Run' Immediate start without trigger signal 'IF Power' Trigger by IF power steps 'Base1: External TRIG In' Trigger signal at connector TRIG IN 'AFRF Gen1: ...' Trigger by processed waveform file
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:POWer:SOURce {param}')

	def get_mgap(self) -> float:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:MGAP \n
		Snippet: value: float = driver.trigger.gprfMeasurement.power.get_mgap() \n
		Defines the minimum duration of the power-down periods (gaps) between two triggered power pulses. This setting is
		relevant for trigger source 'IF Power'. \n
			:return: minimum_gap: Range: 0 s to 0.01 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:POWer:MGAP?')
		return Conversions.str_to_float(response)

	def set_mgap(self, minimum_gap: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:MGAP \n
		Snippet: driver.trigger.gprfMeasurement.power.set_mgap(minimum_gap = 1.0) \n
		Defines the minimum duration of the power-down periods (gaps) between two triggered power pulses. This setting is
		relevant for trigger source 'IF Power'. \n
			:param minimum_gap: Range: 0 s to 0.01 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(minimum_gap)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:POWer:MGAP {param}')

	def get_timeout(self) -> float or bool:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:TOUT \n
		Snippet: value: float or bool = driver.trigger.gprfMeasurement.power.get_timeout() \n
		Specifies the time after which an initiated measurement must have received a trigger event. If no trigger event is
		received, the measurement is stopped in remote control mode. In manual operation mode, a trigger timeout is indicated.
		This setting is relevant for the trigger source 'IF Power' and for trigger signals at TRIG IN. \n
			:return: timeout: (float or boolean) Range: 0.01 s to 300 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:POWer:TOUT?')
		return Conversions.str_to_float_or_bool(response)

	def set_timeout(self, timeout: float or bool) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:TOUT \n
		Snippet: driver.trigger.gprfMeasurement.power.set_timeout(timeout = 1.0) \n
		Specifies the time after which an initiated measurement must have received a trigger event. If no trigger event is
		received, the measurement is stopped in remote control mode. In manual operation mode, a trigger timeout is indicated.
		This setting is relevant for the trigger source 'IF Power' and for trigger signals at TRIG IN. \n
			:param timeout: (float or boolean) Range: 0.01 s to 300 s, Unit: s
		"""
		param = Conversions.decimal_or_bool_value_to_str(timeout)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:POWer:TOUT {param}')

	def get_offset(self) -> float:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:OFFSet \n
		Snippet: value: float = driver.trigger.gprfMeasurement.power.get_offset() \n
		Defines a delay time for triggered measurements. The trigger offset delays the start of the measurement relative to the
		trigger event. \n
			:return: offset: Range: 0 s to 1 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:POWer:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:OFFSet \n
		Snippet: driver.trigger.gprfMeasurement.power.set_offset(offset = 1.0) \n
		Defines a delay time for triggered measurements. The trigger offset delays the start of the measurement relative to the
		trigger event. \n
			:param offset: Range: 0 s to 1 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:POWer:OFFSet {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.PowerMode:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:MODE \n
		Snippet: value: enums.PowerMode = driver.trigger.gprfMeasurement.power.get_mode() \n
		Selects the trigger mode for the measurement. This setting is relevant for the trigger source 'IF Power' and for trigger
		signals at TRIG IN. \n
			:return: mode: ONCE | SWEep | ALL ONCE Only the start of the measurement is triggered SWEep Each measurement cycle is triggered ALL Each measurement interval is triggered
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:POWer:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.PowerMode)

	def set_mode(self, mode: enums.PowerMode) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:MODE \n
		Snippet: driver.trigger.gprfMeasurement.power.set_mode(mode = enums.PowerMode.ALL) \n
		Selects the trigger mode for the measurement. This setting is relevant for the trigger source 'IF Power' and for trigger
		signals at TRIG IN. \n
			:param mode: ONCE | SWEep | ALL ONCE Only the start of the measurement is triggered SWEep Each measurement cycle is triggered ALL Each measurement interval is triggered
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.PowerMode)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:POWer:MODE {param}')

	def get_threshold(self) -> float:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:THReshold \n
		Snippet: value: float = driver.trigger.gprfMeasurement.power.get_threshold() \n
		Defines the trigger threshold for trigger source 'IF Power'. \n
			:return: threshold: Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to expected power minus external attenuation)
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:POWer:THReshold?')
		return Conversions.str_to_float(response)

	def set_threshold(self, threshold: float) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:THReshold \n
		Snippet: driver.trigger.gprfMeasurement.power.set_threshold(threshold = 1.0) \n
		Defines the trigger threshold for trigger source 'IF Power'. \n
			:param threshold: Range: -50 dB to 0 dB, Unit: dB (full scale, i.e. relative to expected power minus external attenuation)
		"""
		param = Conversions.decimal_value_to_str(threshold)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:POWer:THReshold {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlopeExt:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:SLOPe \n
		Snippet: value: enums.SignalSlopeExt = driver.trigger.gprfMeasurement.power.get_slope() \n
		Selects whether the trigger event is generated at the rising or at the falling edge of the trigger pulse. This command is
		relevant for the trigger source 'IF Power'. \n
			:return: event: REDGe | FEDGe | RISing | FALLing REDGe, RISing Rising edge FEDGe, FALLing Falling edge
		"""
		response = self._core.io.query_str('TRIGger:GPRF:MEASurement<Instance>:POWer:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlopeExt)

	def set_slope(self, event: enums.SignalSlopeExt) -> None:
		"""SCPI: TRIGger:GPRF:MEASurement<Instance>:POWer:SLOPe \n
		Snippet: driver.trigger.gprfMeasurement.power.set_slope(event = enums.SignalSlopeExt.FALLing) \n
		Selects whether the trigger event is generated at the rising or at the falling edge of the trigger pulse. This command is
		relevant for the trigger source 'IF Power'. \n
			:param event: REDGe | FEDGe | RISing | FALLing REDGe, RISing Rising edge FEDGe, FALLing Falling edge
		"""
		param = Conversions.enum_scalar_to_str(event, enums.SignalSlopeExt)
		self._core.io.write(f'TRIGger:GPRF:MEASurement<Instance>:POWer:SLOPe {param}')

	def clone(self) -> 'Power':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Power(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
