from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	@property
	def bandpass(self):
		"""bandpass commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_bandpass'):
			from .Bandpass import Bandpass
			self._bandpass = Bandpass(self._core, self._cmd_group)
		return self._bandpass

	@property
	def gauss(self):
		"""gauss commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gauss'):
			from .Gauss import Gauss
			self._gauss = Gauss(self._core, self._cmd_group)
		return self._gauss

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.RbwFilterType:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:TYPE \n
		Snippet: value: enums.RbwFilterType = driver.configure.gprfMeasurement.iqRecorder.filterPy.get_type_py() \n
		Selects the IF filter type. \n
			:return: filter_type: BANDpass | GAUSs BANDpass Bandpass filter with selectable bandwidth GAUSs Gaussian filter with selectable bandwidth
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.RbwFilterType)

	def set_type_py(self, filter_type: enums.RbwFilterType) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:TYPE \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.filterPy.set_type_py(filter_type = enums.RbwFilterType.BANDpass) \n
		Selects the IF filter type. \n
			:param filter_type: BANDpass | GAUSs BANDpass Bandpass filter with selectable bandwidth GAUSs Gaussian filter with selectable bandwidth
		"""
		param = Conversions.enum_scalar_to_str(filter_type, enums.RbwFilterType)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FILTer:TYPE {param}')

	def clone(self) -> 'FilterPy':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FilterPy(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
