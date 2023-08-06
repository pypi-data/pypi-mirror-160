from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Interferer:
	"""Interferer commands group definition. 9 total commands, 3 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("interferer", core, parent)

	@property
	def rf(self):
		"""rf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rf'):
			from .Rf import Rf
			self._rf = Rf(self._core, self._cmd_group)
		return self._rf

	@property
	def modulator(self):
		"""modulator commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_modulator'):
			from .Modulator import Modulator
			self._modulator = Modulator(self._core, self._cmd_group)
		return self._modulator

	@property
	def af(self):
		"""af commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_af'):
			from .Af import Af
			self._af = Af(self._core, self._cmd_group)
		return self._af

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.InterfererMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:MODE \n
		Snippet: value: enums.InterfererMode = driver.source.afRf.generator.interferer.get_mode() \n
		Selects the interferer signal mode. The interferer signal can be an unmodulated CW signal or a modulated signal, carrying
		a single tone. \n
			:return: interferer_mode: NONE | CW | FM | PM | AM NONE Interferer signal disabled CW Unmodulated RF carrier signal FM, PM, AM Frequency / phase / amplitude modulation
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:IFERer:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.InterfererMode)

	def set_mode(self, interferer_mode: enums.InterfererMode) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:MODE \n
		Snippet: driver.source.afRf.generator.interferer.set_mode(interferer_mode = enums.InterfererMode.AM) \n
		Selects the interferer signal mode. The interferer signal can be an unmodulated CW signal or a modulated signal, carrying
		a single tone. \n
			:param interferer_mode: NONE | CW | FM | PM | AM NONE Interferer signal disabled CW Unmodulated RF carrier signal FM, PM, AM Frequency / phase / amplitude modulation
		"""
		param = Conversions.enum_scalar_to_str(interferer_mode, enums.InterfererMode)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IFERer:MODE {param}')

	def get_dfrequency(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:DFRequency \n
		Snippet: value: float = driver.source.afRf.generator.interferer.get_dfrequency() \n
		Specifies the center RF carrier frequency of the interferer. The frequency is specified as offset value relative to the
		center carrier frequency of the wanted signal, configured via method RsCma.Source.AfRf.Generator.RfSettings.frequency. \n
			:return: frequency: Range: -10 MHz to 10 MHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:IFERer:DFRequency?')
		return Conversions.str_to_float(response)

	def set_dfrequency(self, frequency: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:DFRequency \n
		Snippet: driver.source.afRf.generator.interferer.set_dfrequency(frequency = 1.0) \n
		Specifies the center RF carrier frequency of the interferer. The frequency is specified as offset value relative to the
		center carrier frequency of the wanted signal, configured via method RsCma.Source.AfRf.Generator.RfSettings.frequency. \n
			:param frequency: Range: -10 MHz to 10 MHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IFERer:DFRequency {param}')

	def get_dlevel(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:DLEVel \n
		Snippet: value: float = driver.source.afRf.generator.interferer.get_dlevel() \n
		Sets the RMS level of the interferer RF signal. The level is specified as offset value relative to the level of the
		wanted signal, configured via method RsCma.Source.AfRf.Generator.RfSettings.level. \n
			:return: level: Range: -80 dB to 80 dB, Unit: dB
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:IFERer:DLEVel?')
		return Conversions.str_to_float(response)

	def set_dlevel(self, level: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IFERer:DLEVel \n
		Snippet: driver.source.afRf.generator.interferer.set_dlevel(level = 1.0) \n
		Sets the RMS level of the interferer RF signal. The level is specified as offset value relative to the level of the
		wanted signal, configured via method RsCma.Source.AfRf.Generator.RfSettings.level. \n
			:param level: Range: -80 dB to 80 dB, Unit: dB
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IFERer:DLEVel {param}')

	def clone(self) -> 'Interferer':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Interferer(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
