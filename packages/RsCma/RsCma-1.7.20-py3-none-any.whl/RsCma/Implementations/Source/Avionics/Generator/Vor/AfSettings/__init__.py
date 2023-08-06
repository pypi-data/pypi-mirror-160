from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AfSettings:
	"""AfSettings commands group definition. 13 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("afSettings", core, parent)

	@property
	def audioOutput(self):
		"""audioOutput commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_audioOutput'):
			from .AudioOutput import AudioOutput
			self._audioOutput = AudioOutput(self._core, self._cmd_group)
		return self._audioOutput

	@property
	def reference(self):
		"""reference commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_reference'):
			from .Reference import Reference
			self._reference = Reference(self._core, self._cmd_group)
		return self._reference

	@property
	def vphase(self):
		"""vphase commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_vphase'):
			from .Vphase import Vphase
			self._vphase = Vphase(self._core, self._cmd_group)
		return self._vphase

	# noinspection PyTypeChecker
	def get_connector(self) -> enums.AudioConnector:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:CONNector \n
		Snippet: value: enums.AudioConnector = driver.source.avionics.generator.vor.afSettings.get_connector() \n
		Selects the output connector for the generated AF signal (AF1 OUT or AF2 OUT) . \n
			:return: connector: AF1O | AF2O
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:CONNector?')
		return Conversions.str_to_scalar_enum(response, enums.AudioConnector)

	def set_connector(self, connector: enums.AudioConnector) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:CONNector \n
		Snippet: driver.source.avionics.generator.vor.afSettings.set_connector(connector = enums.AudioConnector.AF1O) \n
		Selects the output connector for the generated AF signal (AF1 OUT or AF2 OUT) . \n
			:param connector: AF1O | AF2O
		"""
		param = Conversions.enum_scalar_to_str(connector, enums.AudioConnector)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:CONNector {param}')

	def clone(self) -> 'AfSettings':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = AfSettings(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
