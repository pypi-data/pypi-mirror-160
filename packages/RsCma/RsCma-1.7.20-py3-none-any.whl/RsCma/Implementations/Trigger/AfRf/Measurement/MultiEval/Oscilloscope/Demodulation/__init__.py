from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 11 total commands, 4 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("demodulation", core, parent)

	@property
	def fdeviation(self):
		"""fdeviation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._cmd_group)
		return self._fdeviation

	@property
	def pdeviation(self):
		"""pdeviation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdeviation'):
			from .Pdeviation import Pdeviation
			self._pdeviation = Pdeviation(self._core, self._cmd_group)
		return self._pdeviation

	@property
	def modDepth(self):
		"""modDepth commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_modDepth'):
			from .ModDepth import ModDepth
			self._modDepth = ModDepth(self._core, self._cmd_group)
		return self._modDepth

	@property
	def ssb(self):
		"""ssb commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssb'):
			from .Ssb import Ssb
			self._ssb = Ssb(self._core, self._cmd_group)
		return self._ssb

	# noinspection PyTypeChecker
	def get_source(self) -> enums.TriggerSourceDemod:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:SOURce \n
		Snippet: value: enums.TriggerSourceDemod = driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.get_source() \n
		Selects a trigger event source for the RF input path. \n
			:return: trigger_source: LEFT | RIGHt | DEMod LEFT, RIGHt: left or right channel, for FM stereo only DEMod: demodulator output, not for FM stereo
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerSourceDemod)

	def set_source(self, trigger_source: enums.TriggerSourceDemod) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:SOURce \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.set_source(trigger_source = enums.TriggerSourceDemod.DEMod) \n
		Selects a trigger event source for the RF input path. \n
			:param trigger_source: LEFT | RIGHt | DEMod LEFT, RIGHt: left or right channel, for FM stereo only DEMod: demodulator output, not for FM stereo
		"""
		param = Conversions.enum_scalar_to_str(trigger_source, enums.TriggerSourceDemod)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:SOURce {param}')

	# noinspection PyTypeChecker
	def get_coupling(self) -> enums.TriggerCouplingDemod:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:COUPling \n
		Snippet: value: enums.TriggerCouplingDemod = driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.get_coupling() \n
		Couples the trigger settings for the RF input path to the trigger settings for another path. \n
			:return: trigger_coupling: NONE | AIN | SIN | VOIP No coupling, coupling to AF path, to SPDIF path, to VoIP path
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:COUPling?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerCouplingDemod)

	def set_coupling(self, trigger_coupling: enums.TriggerCouplingDemod) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:COUPling \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.set_coupling(trigger_coupling = enums.TriggerCouplingDemod.AIN) \n
		Couples the trigger settings for the RF input path to the trigger settings for another path. \n
			:param trigger_coupling: NONE | AIN | SIN | VOIP No coupling, coupling to AF path, to SPDIF path, to VoIP path
		"""
		param = Conversions.enum_scalar_to_str(trigger_coupling, enums.TriggerCouplingDemod)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:COUPling {param}')

	# noinspection PyTypeChecker
	def get_state(self) -> enums.ArmedState:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:STATe \n
		Snippet: value: enums.ArmedState = driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.get_state() \n
		Queries the state of the trigger system. \n
			:return: armed_state: OFF | ARMed | TRIGgered OFF The trigger system is disabled. The oscilloscope works as free-run measurement. ARMed The trigger system is armed and waits for a trigger event. TRIGgered A trigger event has occurred. The trigger system has not (yet) been rearmed.
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.ArmedState)

	def get_enable(self) -> bool:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:ENABle \n
		Snippet: value: bool = driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.get_enable() \n
		No command help available \n
			:return: enable: No help available
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:ENABle \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.set_enable(enable = False) \n
		No command help available \n
			:param enable: No help available
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:ENABle {param}')

	def get_offset(self) -> float:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:OFFSet \n
		Snippet: value: float = driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.get_offset() \n
		Defines a trigger offset, shifting the measured trace relative to the trigger event, so that the trace starts earlier.
		The offset is specified as a percentage of the measurement time for a single trace. \n
			:return: trigger_offset: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, trigger_offset: float) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:OFFSet \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.set_offset(trigger_offset = 1.0) \n
		Defines a trigger offset, shifting the measured trace relative to the trigger event, so that the trace starts earlier.
		The offset is specified as a percentage of the measurement time for a single trace. \n
			:param trigger_offset: Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(trigger_offset)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:OFFSet {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.SignalSlope:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:SLOPe \n
		Snippet: value: enums.SignalSlope = driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.get_slope() \n
		Selects whether the trigger event is generated by signals rising through the threshold or falling through the threshold. \n
			:return: trigger_slope: REDGe | FEDGe REDGe Rising signal (rising edge) FEDGe Falling signal (falling edge)
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.SignalSlope)

	def set_slope(self, trigger_slope: enums.SignalSlope) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:SLOPe \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.set_slope(trigger_slope = enums.SignalSlope.FEDGe) \n
		Selects whether the trigger event is generated by signals rising through the threshold or falling through the threshold. \n
			:param trigger_slope: REDGe | FEDGe REDGe Rising signal (rising edge) FEDGe Falling signal (falling edge)
		"""
		param = Conversions.enum_scalar_to_str(trigger_slope, enums.SignalSlope)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:SLOPe {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.TriggerMode:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:MODE \n
		Snippet: value: enums.TriggerMode = driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.get_mode() \n
		Selects the repetition mode of the trigger system. \n
			:return: trigger_mode: SINGle | NORMal | AUTO | FRUN
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.TriggerMode)

	def set_mode(self, trigger_mode: enums.TriggerMode) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:MODE \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.set_mode(trigger_mode = enums.TriggerMode.AUTO) \n
		Selects the repetition mode of the trigger system. \n
			:param trigger_mode: SINGle | NORMal | AUTO | FRUN
		"""
		param = Conversions.enum_scalar_to_str(trigger_mode, enums.TriggerMode)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:MODE {param}')

	def clone(self) -> 'Demodulation':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Demodulation(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
