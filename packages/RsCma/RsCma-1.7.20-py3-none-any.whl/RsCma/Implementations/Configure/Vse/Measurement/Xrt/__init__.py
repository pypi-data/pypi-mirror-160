from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Xrt:
	"""Xrt commands group definition. 4 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("xrt", core, parent)

	@property
	def rfSettings(self):
		"""rfSettings commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_rfSettings'):
			from .RfSettings import RfSettings
			self._rfSettings = RfSettings(self._core, self._cmd_group)
		return self._rfSettings

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:XRT:ENABle \n
		Snippet: value: bool = driver.configure.vse.measurement.xrt.get_enable() \n
		Enables receiving of VSE measurement results via the CMA-XRT100 configuration. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:XRT:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:XRT:ENABle \n
		Snippet: driver.configure.vse.measurement.xrt.set_enable(enable = False) \n
		Enables receiving of VSE measurement results via the CMA-XRT100 configuration. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:XRT:ENABle {param}')

	def clone(self) -> 'Xrt':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Xrt(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
