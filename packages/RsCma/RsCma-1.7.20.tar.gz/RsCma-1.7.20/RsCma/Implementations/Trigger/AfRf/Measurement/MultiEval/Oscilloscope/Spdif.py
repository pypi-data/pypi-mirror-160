from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spdif:
	"""Spdif commands group definition. 8 total commands, 0 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spdif", core, parent)

	# noinspection PyTypeChecker
	def get_source(self) -> enums.LeftRightDirection:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:SOURce \n
		Snippet: value: enums.LeftRightDirection = driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.get_source() \n
		Selects a trigger event source for the SPDIF input path. \n
			:return: trigger_source: LEFT | RIGHt Left or right SPDIF channel
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.LeftRightDirection)

	def set_source(self, trigger_source: enums.LeftRightDirection) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:SOURce \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.set_source(trigger_source = enums.LeftRightDirection.LEFT) \n
		Selects a trigger event source for the SPDIF input path. \n
			:param trigger_source: LEFT | RIGHt Left or right SPDIF channel
		"""
		param = Conversions.enum_scalar_to_str(trigger_source, enums.LeftRightDirection)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:SOURce {param}')

	# noinspection PyTypeChecker
	def get_coupling(self) -> enums.TriggerCouplingDigital:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:COUPling \n
		Snippet: value: enums.TriggerCouplingDigital = driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.get_coupling() \n
		Couples the trigger settings for the SPDIF input path to the trigger settings for another path. \n
			:return: trigger_coupling: NONE | DEMod | AIN No coupling, coupling to RF path or to AF path
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:COUPling?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerCouplingDigital)

	def set_coupling(self, trigger_coupling: enums.TriggerCouplingDigital) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:COUPling \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.set_coupling(trigger_coupling = enums.TriggerCouplingDigital.AIN) \n
		Couples the trigger settings for the SPDIF input path to the trigger settings for another path. \n
			:param trigger_coupling: NONE | DEMod | AIN No coupling, coupling to RF path or to AF path
		"""
		param = Conversions.enum_scalar_to_str(trigger_coupling, enums.TriggerCouplingDigital)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:COUPling {param}')

	# noinspection PyTypeChecker
	def get_state(self) -> enums.ArmedState:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:STATe \n
		Snippet: value: enums.ArmedState = driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.get_state() \n
		Queries the state of the trigger system. \n
			:return: armed_state: OFF | ARMed | TRIGgered OFF The trigger system is disabled. The oscilloscope works as free-run measurement. ARMed The trigger system is armed and waits for a trigger event. TRIGgered A trigger event has occurred. The trigger system has not (yet) been rearmed.
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.ArmedState)

	def get_enable(self) -> bool:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:ENABle \n
		Snippet: value: bool = driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.get_enable() \n
		No command help available \n
			:return: enable: No help available
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:ENABle \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.set_enable(enable = False) \n
		No command help available \n
			:param enable: No help available
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:ENABle {param}')

	def get_offset(self) -> float:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:OFFSet \n
		Snippet: value: float = driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.get_offset() \n
		Defines a trigger offset, shifting the measured trace relative to the trigger event, so that the trace starts earlier.
		The offset is specified as a percentage of the measurement time for a single trace. \n
			:return: trigger_offset: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, trigger_offset: float) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:OFFSet \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.set_offset(trigger_offset = 1.0) \n
		Defines a trigger offset, shifting the measured trace relative to the trigger event, so that the trace starts earlier.
		The offset is specified as a percentage of the measurement time for a single trace. \n
			:param trigger_offset: Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(trigger_offset)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:OFFSet {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlope:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:SLOPe \n
		Snippet: value: enums.SignalSlope = driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.get_slope() \n
		Selects whether the trigger event is generated by signals rising through the threshold or falling through the threshold. \n
			:return: trigger_slope: REDGe | FEDGe REDGe Rising signal (rising edge) FEDGe Falling signal (falling edge)
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlope)

	def set_slope(self, trigger_slope: enums.SignalSlope) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:SLOPe \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.set_slope(trigger_slope = enums.SignalSlope.FEDGe) \n
		Selects whether the trigger event is generated by signals rising through the threshold or falling through the threshold. \n
			:param trigger_slope: REDGe | FEDGe REDGe Rising signal (rising edge) FEDGe Falling signal (falling edge)
		"""
		param = Conversions.enum_scalar_to_str(trigger_slope, enums.SignalSlope)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:SLOPe {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.TriggerMode:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:MODE \n
		Snippet: value: enums.TriggerMode = driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.get_mode() \n
		Selects the repetition mode of the trigger system. \n
			:return: trigger_mode: SINGle | NORMal | AUTO | FRUN
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerMode)

	def set_mode(self, trigger_mode: enums.TriggerMode) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:MODE \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.set_mode(trigger_mode = enums.TriggerMode.AUTO) \n
		Selects the repetition mode of the trigger system. \n
			:param trigger_mode: SINGle | NORMal | AUTO | FRUN
		"""
		param = Conversions.enum_scalar_to_str(trigger_mode, enums.TriggerMode)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:MODE {param}')

	def get_threshold(self) -> float:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:THReshold \n
		Snippet: value: float = driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.get_threshold() \n
		Defines the trigger threshold for the SPDIF input path. \n
			:return: threshold: Audio level threshold Range: -100 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:THReshold?')
		return Conversions.str_to_float(response)

	def set_threshold(self, threshold: float) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:THReshold \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.spdif.set_threshold(threshold = 1.0) \n
		Defines the trigger threshold for the SPDIF input path. \n
			:param threshold: Audio level threshold Range: -100 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(threshold)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:SIN:THReshold {param}')
