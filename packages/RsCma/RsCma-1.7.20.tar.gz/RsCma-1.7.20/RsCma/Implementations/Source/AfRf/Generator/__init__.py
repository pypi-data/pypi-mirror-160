from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Generator:
	"""Generator commands group definition. 237 total commands, 23 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("generator", core, parent)

	@property
	def reliability(self):
		"""reliability commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_reliability'):
			from .Reliability import Reliability
			self._reliability = Reliability(self._core, self._cmd_group)
		return self._reliability

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._cmd_group)
		return self._state

	@property
	def digital(self):
		"""digital commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_digital'):
			from .Digital import Digital
			self._digital = Digital(self._core, self._cmd_group)
		return self._digital

	@property
	def dmr(self):
		"""dmr commands group. 0 Sub-classes, 10 commands."""
		if not hasattr(self, '_dmr'):
			from .Dmr import Dmr
			self._dmr = Dmr(self._core, self._cmd_group)
		return self._dmr

	@property
	def nxdn(self):
		"""nxdn commands group. 0 Sub-classes, 11 commands."""
		if not hasattr(self, '_nxdn'):
			from .Nxdn import Nxdn
			self._nxdn = Nxdn(self._core, self._cmd_group)
		return self._nxdn

	@property
	def pocsag(self):
		"""pocsag commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_pocsag'):
			from .Pocsag import Pocsag
			self._pocsag = Pocsag(self._core, self._cmd_group)
		return self._pocsag

	@property
	def ptFive(self):
		"""ptFive commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_ptFive'):
			from .PtFive import PtFive
			self._ptFive = PtFive(self._core, self._cmd_group)
		return self._ptFive

	@property
	def userDefined(self):
		"""userDefined commands group. 0 Sub-classes, 14 commands."""
		if not hasattr(self, '_userDefined'):
			from .UserDefined import UserDefined
			self._userDefined = UserDefined(self._core, self._cmd_group)
		return self._userDefined

	@property
	def zigbee(self):
		"""zigbee commands group. 0 Sub-classes, 9 commands."""
		if not hasattr(self, '_zigbee'):
			from .Zigbee import Zigbee
			self._zigbee = Zigbee(self._core, self._cmd_group)
		return self._zigbee

	@property
	def dpmr(self):
		"""dpmr commands group. 1 Sub-classes, 11 commands."""
		if not hasattr(self, '_dpmr'):
			from .Dpmr import Dpmr
			self._dpmr = Dpmr(self._core, self._cmd_group)
		return self._dpmr

	@property
	def voip(self):
		"""voip commands group. 3 Sub-classes, 8 commands."""
		if not hasattr(self, '_voip'):
			from .Voip import Voip
			self._voip = Voip(self._core, self._cmd_group)
		return self._voip

	@property
	def audioOutput(self):
		"""audioOutput commands group. 5 Sub-classes, 1 commands."""
		if not hasattr(self, '_audioOutput'):
			from .AudioOutput import AudioOutput
			self._audioOutput = AudioOutput(self._core, self._cmd_group)
		return self._audioOutput

	@property
	def sout(self):
		"""sout commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_sout'):
			from .Sout import Sout
			self._sout = Sout(self._core, self._cmd_group)
		return self._sout

	@property
	def rfSettings(self):
		"""rfSettings commands group. 2 Sub-classes, 9 commands."""
		if not hasattr(self, '_rfSettings'):
			from .RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._cmd_group)
		return self._rfSettings

	@property
	def modulator(self):
		"""modulator commands group. 2 Sub-classes, 4 commands."""
		if not hasattr(self, '_modulator'):
			from .Modulator import Modulator
			self._modulator = Modulator(self._core, self._cmd_group)
		return self._modulator

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._cmd_group)
		return self._filterPy

	@property
	def internalGenerator(self):
		"""internalGenerator commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_internalGenerator'):
			from .InternalGenerator import InternalGenerator
			self._internalGenerator = InternalGenerator(self._core, self._cmd_group)
		return self._internalGenerator

	@property
	def dialing(self):
		"""dialing commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_dialing'):
			from .Dialing import Dialing
			self._dialing = Dialing(self._core, self._cmd_group)
		return self._dialing

	@property
	def audioInput(self):
		"""audioInput commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._cmd_group)
		return self._audioInput

	@property
	def tones(self):
		"""tones commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_tones'):
			from .Tones import Tones
			self._tones = Tones(self._core, self._cmd_group)
		return self._tones

	@property
	def cdefinition(self):
		"""cdefinition commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_cdefinition'):
			from .Cdefinition import Cdefinition
			self._cdefinition = Cdefinition(self._core, self._cmd_group)
		return self._cdefinition

	@property
	def arb(self):
		"""arb commands group. 3 Sub-classes, 6 commands."""
		if not hasattr(self, '_arb'):
			from .Arb import Arb
			self._arb = Arb(self._core, self._cmd_group)
		return self._arb

	@property
	def interferer(self):
		"""interferer commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_interferer'):
			from .Interferer import Interferer
			self._interferer = Interferer(self._core, self._cmd_group)
		return self._interferer

	# noinspection PyTypeChecker
	def get_dsource(self) -> enums.DigitalSource:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DSOurce \n
		Snippet: value: enums.DigitalSource = driver.source.afRf.generator.get_dsource() \n
		Selects the data source for digital scenarios. \n
			:return: dsource: DMR | ARB | NXDN | POCSag | P25 | UDEFined | ZIGBee | DPMR
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DSOurce?')
		return Conversions.str_to_scalar_enum(response, enums.DigitalSource)

	def set_dsource(self, dsource: enums.DigitalSource) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DSOurce \n
		Snippet: driver.source.afRf.generator.set_dsource(dsource = enums.DigitalSource.ARB) \n
		Selects the data source for digital scenarios. \n
			:param dsource: DMR | ARB | NXDN | POCSag | P25 | UDEFined | ZIGBee | DPMR
		"""
		param = Conversions.enum_scalar_to_str(dsource, enums.DigitalSource)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DSOurce {param}')

	# noinspection PyTypeChecker
	def get_mscheme(self) -> enums.ModulationScheme:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MSCHeme \n
		Snippet: value: enums.ModulationScheme = driver.source.afRf.generator.get_mscheme() \n
		Selects the RF signal mode (modulation scheme) for analog scenarios. \n
			:return: mod_scheme: FMSTereo | FM | AM | USB | LSB | PM | CW | ARB FMSTereo FM stereo multiplex signal FM, PM, AM Frequency / phase / amplitude modulation USB, LSB Single sideband modulation, upper / lower sideband CW Constant wave signal (unmodulated RF carrier) ARB Waveform file (ARB file)
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:MSCHeme?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationScheme)

	def set_mscheme(self, mod_scheme: enums.ModulationScheme) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MSCHeme \n
		Snippet: driver.source.afRf.generator.set_mscheme(mod_scheme = enums.ModulationScheme.AM) \n
		Selects the RF signal mode (modulation scheme) for analog scenarios. \n
			:param mod_scheme: FMSTereo | FM | AM | USB | LSB | PM | CW | ARB FMSTereo FM stereo multiplex signal FM, PM, AM Frequency / phase / amplitude modulation USB, LSB Single sideband modulation, upper / lower sideband CW Constant wave signal (unmodulated RF carrier) ARB Waveform file (ARB file)
		"""
		param = Conversions.enum_scalar_to_str(mod_scheme, enums.ModulationScheme)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:MSCHeme {param}')

	def clone(self) -> 'Generator':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Generator(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
