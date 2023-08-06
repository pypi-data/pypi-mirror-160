from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tetra:
	"""Tetra commands group definition. 4 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tetra", core, parent)

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._cmd_group)
		return self._filterPy

	def get_symbol_rate(self) -> int:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:TETRa:SRATe \n
		Snippet: value: int = driver.configure.vse.measurement.tetra.get_symbol_rate() \n
		Queries the symbol rate for TETRA. \n
			:return: symbol_rate: No help available
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:TETRa:SRATe?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_demodulation(self) -> enums.DemodulationType:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:TETRa:DEModulation \n
		Snippet: value: enums.DemodulationType = driver.configure.vse.measurement.tetra.get_demodulation() \n
		Queries the modulation type used for TETRA. \n
			:return: demodulation_type: FSK4
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:TETRa:DEModulation?')
		return Conversions.str_to_scalar_enum(response, enums.DemodulationType)

	def clone(self) -> 'Tetra':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tetra(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
