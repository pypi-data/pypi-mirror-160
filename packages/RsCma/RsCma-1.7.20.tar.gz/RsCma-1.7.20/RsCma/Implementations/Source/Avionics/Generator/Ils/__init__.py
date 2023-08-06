from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ils:
	"""Ils commands group definition. 37 total commands, 3 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ils", core, parent)

	@property
	def localizer(self):
		"""localizer commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_localizer'):
			from .Localizer import Localizer
			self._localizer = Localizer(self._core, self._cmd_group)
		return self._localizer

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._cmd_group)
		return self._state

	@property
	def gslope(self):
		"""gslope commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_gslope'):
			from .Gslope import Gslope
			self._gslope = Gslope(self._core, self._cmd_group)
		return self._gslope

	def get_fpairment(self) -> bool:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:FPAirment \n
		Snippet: value: bool = driver.source.avionics.generator.ils.get_fpairment() \n
		Enables or disables 'Frequency Pairment', that is the coupling between the glide slope carrier frequency and the
		localizer carrier frequency. \n
			:return: pairment: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS:FPAirment?')
		return Conversions.str_to_bool(response)

	def set_fpairment(self, pairment: bool) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:FPAirment \n
		Snippet: driver.source.avionics.generator.ils.set_fpairment(pairment = False) \n
		Enables or disables 'Frequency Pairment', that is the coupling between the glide slope carrier frequency and the
		localizer carrier frequency. \n
			:param pairment: OFF | ON
		"""
		param = Conversions.bool_to_str(pairment)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:FPAirment {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.IlsTab:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS \n
		Snippet: value: enums.IlsTab = driver.source.avionics.generator.ils.get_value() \n
		Selects the ILS generator subtab to be displayed at the GUI. \n
			:return: ils_tab: LOCalizer | GSLope
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS?')
		return Conversions.str_to_scalar_enum(response, enums.IlsTab)

	def set_value(self, ils_tab: enums.IlsTab) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS \n
		Snippet: driver.source.avionics.generator.ils.set_value(ils_tab = enums.IlsTab.GSLope) \n
		Selects the ILS generator subtab to be displayed at the GUI. \n
			:param ils_tab: LOCalizer | GSLope
		"""
		param = Conversions.enum_scalar_to_str(ils_tab, enums.IlsTab)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS {param}')

	def clone(self) -> 'Ils':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ils(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
