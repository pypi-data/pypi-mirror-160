from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Display:
	"""Display commands group definition. 12 total commands, 4 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("display", core, parent)

	@property
	def afRf(self):
		"""afRf commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_afRf'):
			from .AfRf import AfRf
			self._afRf = AfRf(self._core, self._cmd_group)
		return self._afRf

	@property
	def gprfMeasurement(self):
		"""gprfMeasurement commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_gprfMeasurement'):
			from .GprfMeasurement import GprfMeasurement
			self._gprfMeasurement = GprfMeasurement(self._core, self._cmd_group)
		return self._gprfMeasurement

	@property
	def window(self):
		"""window commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_window'):
			from .Window import Window
			self._window = Window(self._core, self._cmd_group)
		return self._window

	@property
	def vse(self):
		"""vse commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_vse'):
			from .Vse import Vse
			self._vse = Vse(self._core, self._cmd_group)
		return self._vse

	def get_format_py(self) -> str:
		"""SCPI: DISPlay:FORMat \n
		Snippet: value: str = driver.display.get_format_py() \n
		No command help available \n
			:return: arg_0: No help available
		"""
		response = self._core.io.query_str('DISPlay:FORMat?')
		return trim_str_response(response)

	def set_format_py(self, arg_0: str) -> None:
		"""SCPI: DISPlay:FORMat \n
		Snippet: driver.display.set_format_py(arg_0 = r1) \n
		No command help available \n
			:param arg_0: No help available
		"""
		param = Conversions.value_to_str(arg_0)
		self._core.io.write(f'DISPlay:FORMat {param}')

	def clone(self) -> 'Display':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Display(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
