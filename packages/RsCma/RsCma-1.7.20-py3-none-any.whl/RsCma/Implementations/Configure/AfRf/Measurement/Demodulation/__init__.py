from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 35 total commands, 8 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("demodulation", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Frequency import Frequency
			self._frequency = Frequency(self._core, self._cmd_group)
		return self._frequency

	@property
	def fmStereo(self):
		"""fmStereo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fmStereo'):
			from .FmStereo import FmStereo
			self._fmStereo = FmStereo(self._core, self._cmd_group)
		return self._fmStereo

	@property
	def modDepth(self):
		"""modDepth commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_modDepth'):
			from .ModDepth import ModDepth
			self._modDepth = ModDepth(self._core, self._cmd_group)
		return self._modDepth

	@property
	def fdeviation(self):
		"""fdeviation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._cmd_group)
		return self._fdeviation

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import Enable
			self._enable = Enable(self._core, self._cmd_group)
		return self._enable

	@property
	def gcoupling(self):
		"""gcoupling commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gcoupling'):
			from .Gcoupling import Gcoupling
			self._gcoupling = Gcoupling(self._core, self._cmd_group)
		return self._gcoupling

	@property
	def tmode(self):
		"""tmode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tmode'):
			from .Tmode import Tmode
			self._tmode = Tmode(self._core, self._cmd_group)
		return self._tmode

	@property
	def filterPy(self):
		"""filterPy commands group. 4 Sub-classes, 6 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._cmd_group)
		return self._filterPy

	# noinspection PyTypeChecker
	def get_value(self) -> enums.Demodulation:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation \n
		Snippet: value: enums.Demodulation = driver.configure.afRf.measurement.demodulation.get_value() \n
		Selects the type of demodulation to be performed. \n
			:return: demodulation: FMSTereo | FM | AM | USB | LSB | PM FMSTereo FM stereo multiplex signal FM, PM, AM Frequency / phase / amplitude modulation USB, LSB Single sideband modulation, upper / lower sideband
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation?')
		return Conversions.str_to_scalar_enum(response, enums.Demodulation)

	def set_value(self, demodulation: enums.Demodulation) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation \n
		Snippet: driver.configure.afRf.measurement.demodulation.set_value(demodulation = enums.Demodulation.AM) \n
		Selects the type of demodulation to be performed. \n
			:param demodulation: FMSTereo | FM | AM | USB | LSB | PM FMSTereo FM stereo multiplex signal FM, PM, AM Frequency / phase / amplitude modulation USB, LSB Single sideband modulation, upper / lower sideband
		"""
		param = Conversions.enum_scalar_to_str(demodulation, enums.Demodulation)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation {param}')

	def clone(self) -> 'Demodulation':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Demodulation(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
