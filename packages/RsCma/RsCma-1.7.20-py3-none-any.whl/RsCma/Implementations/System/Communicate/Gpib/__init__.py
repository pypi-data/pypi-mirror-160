from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gpib:
	"""Gpib commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gpib", core, parent)

	@property
	def self(self):
		"""self commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_self'):
			from .Self import Self
			self._self = Self(self._core, self._cmd_group)
		return self._self

	def get_vresource(self) -> str:
		"""SCPI: SYSTem:COMMunicate:GPIB:VRESource \n
		Snippet: value: str = driver.system.communicate.gpib.get_vresource() \n
		Queries the VISA resource string of the GPIB interface. \n
			:return: visa_resource: VISA resource string
		"""
		response = self._core.io.query_str('SYSTem:COMMunicate:GPIB:VRESource?')
		return trim_str_response(response)

	def clone(self) -> 'Gpib':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gpib(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
