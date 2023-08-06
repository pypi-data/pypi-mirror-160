from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nxdn:
	"""Nxdn commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("nxdn", core, parent)

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._cmd_group)
		return self._filterPy

	# noinspection PyTypeChecker
	def get_transmission(self) -> enums.Transmission:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:NXDN:TRANsmission \n
		Snippet: value: enums.Transmission = driver.configure.vse.measurement.nxdn.get_transmission() \n
		Queries the data rate in bits/s for enhanced full rate (EFR) or enhanced half rate (EHR) . \n
			:return: transmission: EHR4800 | EHR9600 | EFR9600
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:NXDN:TRANsmission?')
		return Conversions.str_to_scalar_enum(response, enums.Transmission)

	def set_transmission(self, transmission: enums.Transmission) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:NXDN:TRANsmission \n
		Snippet: driver.configure.vse.measurement.nxdn.set_transmission(transmission = enums.Transmission.EFR9600) \n
		Queries the data rate in bits/s for enhanced full rate (EFR) or enhanced half rate (EHR) . \n
			:param transmission: EHR4800 | EHR9600 | EFR9600
		"""
		param = Conversions.enum_scalar_to_str(transmission, enums.Transmission)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:NXDN:TRANsmission {param}')

	def clone(self) -> 'Nxdn':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nxdn(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
