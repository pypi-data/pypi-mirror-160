from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Generator:
	"""Generator commands group definition. 22 total commands, 5 Subgroups, 1 group commands"""

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
		"""digital commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_digital'):
			from .Digital import Digital
			self._digital = Digital(self._core, self._cmd_group)
		return self._digital

	@property
	def rfSettings(self):
		"""rfSettings commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_rfSettings'):
			from .RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._cmd_group)
		return self._rfSettings

	@property
	def arb(self):
		"""arb commands group. 2 Sub-classes, 6 commands."""
		if not hasattr(self, '_arb'):
			from .Arb import Arb
			self._arb = Arb(self._core, self._cmd_group)
		return self._arb

	# noinspection PyTypeChecker
	def get_dsource(self) -> enums.DigitalSource:
		"""SCPI: SOURce:XRT:GENerator<Instance>:DSOurce \n
		Snippet: value: enums.DigitalSource = driver.source.xrt.generator.get_dsource() \n
		Selects the data source for the XRT generator. \n
			:return: dsource: RF ARB | DMR | NXDN | POCSAG | P25 | ZigBee | DPMR
		"""
		response = self._core.io.query_str('SOURce:XRT:GENerator<Instance>:DSOurce?')
		return Conversions.str_to_scalar_enum(response, enums.DigitalSource)

	def set_dsource(self, dsource: enums.DigitalSource) -> None:
		"""SCPI: SOURce:XRT:GENerator<Instance>:DSOurce \n
		Snippet: driver.source.xrt.generator.set_dsource(dsource = enums.DigitalSource.ARB) \n
		Selects the data source for the XRT generator. \n
			:param dsource: RF ARB | DMR | NXDN | POCSAG | P25 | ZigBee | DPMR
		"""
		param = Conversions.enum_scalar_to_str(dsource, enums.DigitalSource)
		self._core.io.write(f'SOURce:XRT:GENerator<Instance>:DSOurce {param}')

	def clone(self) -> 'Generator':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Generator(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
