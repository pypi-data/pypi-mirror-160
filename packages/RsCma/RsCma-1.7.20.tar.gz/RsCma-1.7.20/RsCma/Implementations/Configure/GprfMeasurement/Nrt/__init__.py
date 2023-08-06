from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nrt:
	"""Nrt commands group definition. 25 total commands, 3 Subgroups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nrt", core, parent)

	@property
	def forward(self):
		"""forward commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_forward'):
			from .Forward import Forward
			self._forward = Forward(self._core, self._cmd_group)
		return self._forward

	@property
	def reverse(self):
		"""reverse commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_reverse'):
			from .Reverse import Reverse
			self._reverse = Reverse(self._core, self._cmd_group)
		return self._reverse

	@property
	def attenuation(self):
		"""attenuation commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_attenuation'):
			from .Attenuation import Attenuation
			self._attenuation = Attenuation(self._core, self._cmd_group)
		return self._attenuation

	def get_scount(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:SCOunt \n
		Snippet: value: int = driver.configure.gprfMeasurement.nrt.get_scount() \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval comprises one set of
		results for both directions. \n
			:return: statistic_count: Range: 1 to 1000
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:SCOunt \n
		Snippet: driver.configure.gprfMeasurement.nrt.set_scount(statistic_count = 1) \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval comprises one set of
		results for both directions. \n
			:param statistic_count: Range: 1 to 1000
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:SCOunt {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.gprfMeasurement.nrt.get_repetition() \n
		Selects whether the measurement is repeated continuously or not. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REPetition \n
		Snippet: driver.configure.gprfMeasurement.nrt.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Selects whether the measurement is repeated continuously or not. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:REPetition {param}')

	def get_rcoupling(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:RCOupling \n
		Snippet: value: bool = driver.configure.gprfMeasurement.nrt.get_rcoupling() \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:return: repetition_coupl: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:RCOupling?')
		return Conversions.str_to_bool(response)

	def set_rcoupling(self, repetition_coupl: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:RCOupling \n
		Snippet: driver.configure.gprfMeasurement.nrt.set_rcoupling(repetition_coupl = False) \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:param repetition_coupl: OFF | ON
		"""
		param = Conversions.bool_to_str(repetition_coupl)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:RCOupling {param}')

	def get_frequency(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FREQuency \n
		Snippet: value: float = driver.configure.gprfMeasurement.nrt.get_frequency() \n
		Specifies the input frequency at the power sensor. \n
			:return: correction_freq: Range: Depends on the power sensor model , Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, correction_freq: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FREQuency \n
		Snippet: driver.configure.gprfMeasurement.nrt.set_frequency(correction_freq = 1.0) \n
		Specifies the input frequency at the power sensor. \n
			:param correction_freq: Range: Depends on the power sensor model , Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(correction_freq)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:FREQuency {param}')

	def get_cumulative_distrib_fnc(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:CCDF \n
		Snippet: value: float = driver.configure.gprfMeasurement.nrt.get_cumulative_distrib_fnc() \n
		Configures a PEP threshold for calculation of the CCDF result. Note the default value dBm. To enter watts, append W to
		the value, for example 2W. To query watts, append a W to your query: CONFigure:GPRF:MEAS:NRT:CCDF? W. \n
			:return: threshold: Range: 1 W to 300 W, Unit: dBm
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:CCDF?')
		return Conversions.str_to_float(response)

	def set_cumulative_distrib_fnc(self, threshold: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:CCDF \n
		Snippet: driver.configure.gprfMeasurement.nrt.set_cumulative_distrib_fnc(threshold = 1.0) \n
		Configures a PEP threshold for calculation of the CCDF result. Note the default value dBm. To enter watts, append W to
		the value, for example 2W. To query watts, append a W to your query: CONFigure:GPRF:MEAS:NRT:CCDF? W. \n
			:param threshold: Range: 1 W to 300 W, Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(threshold)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:CCDF {param}')

	def get_bandwidth(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:BWIDth \n
		Snippet: value: float = driver.configure.gprfMeasurement.nrt.get_bandwidth() \n
		Sets the video filter bandwidth for the rectified RF signal. \n
			:return: bandwidth: The entered value is rounded to the nearest of the following values: 4 kHz | 200 kHz | 600 kHz Range: 4000 Hz to 600 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:BWIDth?')
		return Conversions.str_to_float(response)

	def set_bandwidth(self, bandwidth: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:BWIDth \n
		Snippet: driver.configure.gprfMeasurement.nrt.set_bandwidth(bandwidth = 1.0) \n
		Sets the video filter bandwidth for the rectified RF signal. \n
			:param bandwidth: The entered value is rounded to the nearest of the following values: 4 kHz | 200 kHz | 600 kHz Range: 4000 Hz to 600 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(bandwidth)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:BWIDth {param}')

	# noinspection PyTypeChecker
	def get_resolution(self) -> enums.LowHigh:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:RESolution \n
		Snippet: value: enums.LowHigh = driver.configure.gprfMeasurement.nrt.get_resolution() \n
		Selects the measurement resolution. \n
			:return: bandwidth: LOW | HIGH
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:RESolution?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_resolution(self, bandwidth: enums.LowHigh) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:RESolution \n
		Snippet: driver.configure.gprfMeasurement.nrt.set_resolution(bandwidth = enums.LowHigh.HIGH) \n
		Selects the measurement resolution. \n
			:param bandwidth: LOW | HIGH
		"""
		param = Conversions.enum_scalar_to_str(bandwidth, enums.LowHigh)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:RESolution {param}')

	# noinspection PyTypeChecker
	def get_direction(self) -> enums.PowerSignalDirection:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:DIRection \n
		Snippet: value: enums.PowerSignalDirection = driver.configure.gprfMeasurement.nrt.get_direction() \n
		Defines the forward direction relative to the ports of the power sensor. \n
			:return: direction: FWD | REV | AUTO FWD The forward direction is fixed from port 1 to port 2. REV The forward direction is fixed from port 2 to port 1. AUTO The forward direction is selected automatically.
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.PowerSignalDirection)

	def set_direction(self, direction: enums.PowerSignalDirection) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:DIRection \n
		Snippet: driver.configure.gprfMeasurement.nrt.set_direction(direction = enums.PowerSignalDirection.AUTO) \n
		Defines the forward direction relative to the ports of the power sensor. \n
			:param direction: FWD | REV | AUTO FWD The forward direction is fixed from port 1 to port 2. REV The forward direction is fixed from port 2 to port 1. AUTO The forward direction is selected automatically.
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.PowerSignalDirection)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:DIRection {param}')

	def get_pep_hold_time(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:PEPHoldtime \n
		Snippet: value: float = driver.configure.gprfMeasurement.nrt.get_pep_hold_time() \n
		Sets the hold time for the measurement of the peak envelope power. \n
			:return: pep_hold_time: Range: 1E-3 s to 0.1 s, Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:PEPHoldtime?')
		return Conversions.str_to_float(response)

	def set_pep_hold_time(self, pep_hold_time: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:PEPHoldtime \n
		Snippet: driver.configure.gprfMeasurement.nrt.set_pep_hold_time(pep_hold_time = 1.0) \n
		Sets the hold time for the measurement of the peak envelope power. \n
			:param pep_hold_time: Range: 1E-3 s to 0.1 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(pep_hold_time)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:PEPHoldtime {param}')

	# noinspection PyTypeChecker
	def get_device(self) -> enums.NrtDevice:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:DEVice \n
		Snippet: value: enums.NrtDevice = driver.configure.gprfMeasurement.nrt.get_device() \n
		Selects the used power sensor model. \n
			:return: device: N14 | N43 | N44 N14: R&S NRT-Z14 N43: R&S NRT-Z43 N44: R&S NRT-Z44
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:DEVice?')
		return Conversions.str_to_scalar_enum(response, enums.NrtDevice)

	def set_device(self, device: enums.NrtDevice) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:DEVice \n
		Snippet: driver.configure.gprfMeasurement.nrt.set_device(device = enums.NrtDevice.N14) \n
		Selects the used power sensor model. \n
			:param device: N14 | N43 | N44 N14: R&S NRT-Z14 N43: R&S NRT-Z43 N44: R&S NRT-Z44
		"""
		param = Conversions.enum_scalar_to_str(device, enums.NrtDevice)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:DEVice {param}')

	def clone(self) -> 'Nrt':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nrt(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
