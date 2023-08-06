from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	@property
	def rrc(self):
		"""rrc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rrc'):
			from .Rrc import Rrc
			self._rrc = Rrc(self._core, self._cmd_group)
		return self._rrc

	# noinspection PyTypeChecker
	def get_value(self) -> enums.PulseShapingUserFilter:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:TETRa:FILTer \n
		Snippet: value: enums.PulseShapingUserFilter = driver.configure.vse.measurement.tetra.filterPy.get_value() \n
		Queries the filter type used for pulse shaping for TETRA. \n
			:return: filter_py: RRC
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:TETRa:FILTer?')
		return Conversions.str_to_scalar_enum(response, enums.PulseShapingUserFilter)

	def clone(self) -> 'FilterPy':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPy(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
