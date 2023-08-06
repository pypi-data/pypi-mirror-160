from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Counter:
	"""Counter commands group definition. 14 total commands, 2 Subgroups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("counter", core, parent)

	@property
	def frange(self):
		"""frange commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_frange'):
			from .Frange import Frange
			self._frange = Frange(self._core, self._cmd_group)
		return self._frange

	@property
	def use(self):
		"""use commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_use'):
			from .Use import Use
			self._use = Use(self._core, self._cmd_group)
		return self._use

	# noinspection PyTypeChecker
	def get_detection(self) -> enums.Repeat:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:DETection \n
		Snippet: value: enums.Repeat = driver.configure.afRf.measurement.frequency.counter.get_detection() \n
		Selects whether the search procedure stops after finding an RF signal, or continues. \n
			:return: detection: SINGleshot | CONTinuous SINGleshot If the search procedure finds a signal during a search cycle, it stops after the cycle. CONTinuous The procedure continues searching until you abort the search.
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:DETection?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_detection(self, detection: enums.Repeat) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:DETection \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.set_detection(detection = enums.Repeat.CONTinuous) \n
		Selects whether the search procedure stops after finding an RF signal, or continues. \n
			:param detection: SINGleshot | CONTinuous SINGleshot If the search procedure finds a signal during a search cycle, it stops after the cycle. CONTinuous The procedure continues searching until you abort the search.
		"""
		param = Conversions.enum_scalar_to_str(detection, enums.Repeat)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:DETection {param}')

	def get_afrequency(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:AFRequency \n
		Snippet: value: float = driver.configure.afRf.measurement.frequency.counter.get_afrequency() \n
		Specifies the single-tone audio frequency. Only relevant for SSB. \n
			:return: audio: Range: 1 Hz to 10500 Hz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:AFRequency?')
		return Conversions.str_to_float(response)

	def set_afrequency(self, audio: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:AFRequency \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.set_afrequency(audio = 1.0) \n
		Specifies the single-tone audio frequency. Only relevant for SSB. \n
			:param audio: Range: 1 Hz to 10500 Hz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(audio)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:AFRequency {param}')

	# noinspection PyTypeChecker
	def get_gcoupling(self) -> enums.GeneratorCoupling:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:GCOupling \n
		Snippet: value: enums.GeneratorCoupling = driver.configure.afRf.measurement.frequency.counter.get_gcoupling() \n
		Couples the single-tone audio frequency to an internal signal generator. Only relevant for SSB. \n
			:return: coupling: OFF | GEN1 | GEN2 | GEN3 | GEN4 OFF No coupling GENn Coupled to audio generator n
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:GCOupling?')
		return Conversions.str_to_scalar_enum(response, enums.GeneratorCoupling)

	def set_gcoupling(self, coupling: enums.GeneratorCoupling) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:GCOupling \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.set_gcoupling(coupling = enums.GeneratorCoupling.GEN1) \n
		Couples the single-tone audio frequency to an internal signal generator. Only relevant for SSB. \n
			:param coupling: OFF | GEN1 | GEN2 | GEN3 | GEN4 OFF No coupling GENn Coupled to audio generator n
		"""
		param = Conversions.enum_scalar_to_str(coupling, enums.GeneratorCoupling)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:GCOupling {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.afRf.measurement.frequency.counter.get_repetition() \n
		No command help available \n
			:return: repetition_mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition_mode: enums.Repeat) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:REPetition \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.set_repetition(repetition_mode = enums.Repeat.CONTinuous) \n
		No command help available \n
			:param repetition_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(repetition_mode, enums.Repeat)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:REPetition {param}')

	def get_timeout(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:TOUT \n
		Snippet: value: int = driver.configure.afRf.measurement.frequency.counter.get_timeout() \n
		Specifies a timeout for the search procedure. \n
			:return: timeout: Range: 0 s to 36E+3 s, Unit: s
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:TOUT?')
		return Conversions.str_to_int(response)

	def set_timeout(self, timeout: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:TOUT \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.set_timeout(timeout = 1) \n
		Specifies a timeout for the search procedure. \n
			:param timeout: Range: 0 s to 36E+3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(timeout)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:TOUT {param}')

	def get_spower(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:SPOWer \n
		Snippet: value: float = driver.configure.afRf.measurement.frequency.counter.get_spower() \n
		No command help available \n
			:return: search_power: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:SPOWer?')
		return Conversions.str_to_float(response)

	def set_spower(self, search_power: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:SPOWer \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.set_spower(search_power = 1.0) \n
		No command help available \n
			:param search_power: No help available
		"""
		param = Conversions.decimal_value_to_str(search_power)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:SPOWer {param}')

	def get_automatic(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:AUTomatic \n
		Snippet: value: bool = driver.configure.afRf.measurement.frequency.counter.get_automatic() \n
		Selects whether search results found in 'SingleShot' mode are applied automatically or not. \n
			:return: auto: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:AUTomatic?')
		return Conversions.str_to_bool(response)

	def set_automatic(self, auto: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:AUTomatic \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.set_automatic(auto = False) \n
		Selects whether search results found in 'SingleShot' mode are applied automatically or not. \n
			:param auto: OFF | ON
		"""
		param = Conversions.bool_to_str(auto)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:AUTomatic {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AnalogDigital:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:MODE \n
		Snippet: value: enums.AnalogDigital = driver.configure.afRf.measurement.frequency.counter.get_mode() \n
		Selects, whether the search procedure is used in 'Analog' or 'Digital' scenarios. \n
			:return: mode: ANALog | DIGital
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AnalogDigital)

	def set_mode(self, mode: enums.AnalogDigital) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:MODE \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.set_mode(mode = enums.AnalogDigital.ANALog) \n
		Selects, whether the search procedure is used in 'Analog' or 'Digital' scenarios. \n
			:param mode: ANALog | DIGital
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AnalogDigital)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:MODE {param}')

	def get_fe_power(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FEPower \n
		Snippet: value: bool = driver.configure.afRf.measurement.frequency.counter.get_fe_power() \n
		Fixes the 'Expected Power' for the search procedure. \n
			:return: state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FEPower?')
		return Conversions.str_to_bool(response)

	def set_fe_power(self, state: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FEPower \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.set_fe_power(state = False) \n
		Fixes the 'Expected Power' for the search procedure. \n
			:param state: OFF | ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:FEPower {param}')

	def get_burst(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:BURSt \n
		Snippet: value: bool = driver.configure.afRf.measurement.frequency.counter.get_burst() \n
		Enable burst signal mode for improved detection of pulsed signals or burst signal with the 'Find RF' measurement
		procedure. \n
			:return: state: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:BURSt?')
		return Conversions.str_to_bool(response)

	def set_burst(self, state: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:BURSt \n
		Snippet: driver.configure.afRf.measurement.frequency.counter.set_burst(state = False) \n
		Enable burst signal mode for improved detection of pulsed signals or burst signal with the 'Find RF' measurement
		procedure. \n
			:param state: OFF | ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FREQuency:COUNter:BURSt {param}')

	def clone(self) -> 'Counter':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Counter(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
