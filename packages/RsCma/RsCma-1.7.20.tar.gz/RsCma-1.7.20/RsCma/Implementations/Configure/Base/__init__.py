from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Base:
	"""Base commands group definition. 28 total commands, 11 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("base", core, parent)

	@property
	def sysSound(self):
		"""sysSound commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sysSound'):
			from .SysSound import SysSound
			self._sysSound = SysSound(self._core, self._cmd_group)
		return self._sysSound

	@property
	def cmaSound(self):
		"""cmaSound commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_cmaSound'):
			from .CmaSound import CmaSound
			self._cmaSound = CmaSound(self._core, self._cmd_group)
		return self._cmaSound

	@property
	def attenuation(self):
		"""attenuation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_attenuation'):
			from .Attenuation import Attenuation
			self._attenuation = Attenuation(self._core, self._cmd_group)
		return self._attenuation

	@property
	def cprotection(self):
		"""cprotection commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cprotection'):
			from .Cprotection import Cprotection
			self._cprotection = Cprotection(self._core, self._cmd_group)
		return self._cprotection

	@property
	def adjustment(self):
		"""adjustment commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_adjustment'):
			from .Adjustment import Adjustment
			self._adjustment = Adjustment(self._core, self._cmd_group)
		return self._adjustment

	@property
	def ttl(self):
		"""ttl commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_ttl'):
			from .Ttl import Ttl
			self._ttl = Ttl(self._core, self._cmd_group)
		return self._ttl

	@property
	def display(self):
		"""display commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_display'):
			from .Display import Display
			self._display = Display(self._core, self._cmd_group)
		return self._display

	@property
	def relay(self):
		"""relay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_relay'):
			from .Relay import Relay
			self._relay = Relay(self._core, self._cmd_group)
		return self._relay

	@property
	def zbox(self):
		"""zbox commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_zbox'):
			from .Zbox import Zbox
			self._zbox = Zbox(self._core, self._cmd_group)
		return self._zbox

	@property
	def audioOutput(self):
		"""audioOutput commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioOutput'):
			from .AudioOutput import AudioOutput
			self._audioOutput = AudioOutput(self._core, self._cmd_group)
		return self._audioOutput

	@property
	def audioInput(self):
		"""audioInput commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._cmd_group)
		return self._audioInput

	def get_speaker(self) -> bool:
		"""SCPI: CONFigure:BASE:SPEaker \n
		Snippet: value: bool = driver.configure.base.get_speaker() \n
		Switches the loudspeaker / headphones on or off. \n
			:return: speaker: ON | OFF
		"""
		response = self._core.io.query_str('CONFigure:BASE:SPEaker?')
		return Conversions.str_to_bool(response)

	def set_speaker(self, speaker: bool) -> None:
		"""SCPI: CONFigure:BASE:SPEaker \n
		Snippet: driver.configure.base.set_speaker(speaker = False) \n
		Switches the loudspeaker / headphones on or off. \n
			:param speaker: ON | OFF
		"""
		param = Conversions.bool_to_str(speaker)
		self._core.io.write(f'CONFigure:BASE:SPEaker {param}')

	# noinspection PyTypeChecker
	def get_scenario(self) -> enums.BaseScenario:
		"""SCPI: CONFigure:BASE:SCENario \n
		Snippet: value: enums.BaseScenario = driver.configure.base.get_scenario() \n
		Selects the test scenario. Always select the scenario to be used before configuring and using an application. If you show
		the display during remote control (for example with the 'Hide Remote Screen' button or SYSTem:DISPlay:UPDate ON) , the
		execution of this command takes some seconds. Insert a pause into your test script after this command, to ensure that the
		change has been applied. Or query the setting until the correct new value is returned, before you continue your test
		script. \n
			:return: scenario: TXTest | RXTest | DXTest | SPECtrum | EXPert | AUDio | AVIonics | DTXTest | DRXTest | DSPectrum | DEXPert TXTest | RXTest | DXTest | SPECtrum | EXPert | AUDio | AVIonics Analog scenarios DTXTest | DRXTest | DSPectrum | DEXPert Digital scenarios NOSC Cannot be set, but is returned by a query if no scenario is active.
		"""
		response = self._core.io.query_str_with_opc('CONFigure:BASE:SCENario?')
		return Conversions.str_to_scalar_enum(response, enums.BaseScenario)

	def set_scenario(self, scenario: enums.BaseScenario) -> None:
		"""SCPI: CONFigure:BASE:SCENario \n
		Snippet: driver.configure.base.set_scenario(scenario = enums.BaseScenario.AUDio) \n
		Selects the test scenario. Always select the scenario to be used before configuring and using an application. If you show
		the display during remote control (for example with the 'Hide Remote Screen' button or SYSTem:DISPlay:UPDate ON) , the
		execution of this command takes some seconds. Insert a pause into your test script after this command, to ensure that the
		change has been applied. Or query the setting until the correct new value is returned, before you continue your test
		script. \n
			:param scenario: TXTest | RXTest | DXTest | SPECtrum | EXPert | AUDio | AVIonics | DTXTest | DRXTest | DSPectrum | DEXPert TXTest | RXTest | DXTest | SPECtrum | EXPert | AUDio | AVIonics Analog scenarios DTXTest | DRXTest | DSPectrum | DEXPert Digital scenarios NOSC Cannot be set, but is returned by a query if no scenario is active.
		"""
		param = Conversions.enum_scalar_to_str(scenario, enums.BaseScenario)
		self._core.io.write_with_opc(f'CONFigure:BASE:SCENario {param}')

	def clone(self) -> 'Base':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Base(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
