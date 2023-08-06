from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FmStereo:
	"""FmStereo commands group definition. 4 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fmStereo", core, parent)

	@property
	def madeviation(self):
		"""madeviation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_madeviation'):
			from .Madeviation import Madeviation
			self._madeviation = Madeviation(self._core, self._cmd_group)
		return self._madeviation

	@property
	def pdeviation(self):
		"""pdeviation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdeviation'):
			from .Pdeviation import Pdeviation
			self._pdeviation = Pdeviation(self._core, self._cmd_group)
		return self._pdeviation

	@property
	def rdsDeviation(self):
		"""rdsDeviation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rdsDeviation'):
			from .RdsDeviation import RdsDeviation
			self._rdsDeviation = RdsDeviation(self._core, self._cmd_group)
		return self._rdsDeviation

	def get_mdeviation(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:MDEViation \n
		Snippet: value: float = driver.source.afRf.generator.modulator.fmStereo.get_mdeviation() \n
		Queries the frequency deviation of the FM stereo multiplex signal. The value is calculated from the frequency deviations
		configured for the signal components. \n
			:return: max_freq_deviation: Range: 0 Hz to 100 kHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:MDEViation?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'FmStereo':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FmStereo(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
