from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Out:
	"""Out commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("out", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import Catalog
			self._catalog = Catalog(self._core, self._cmd_group)
		return self._catalog

	def get_source(self) -> str:
		"""SCPI: TRIGger:BASE:OUT:SOURce \n
		Snippet: value: str = driver.trigger.base.out.get_source() \n
		Selects the output trigger signal to be routed to the TRIG OUT connector. \n
			:return: source: Source as string, examples: 'No Connection' TRIG OUT connector deactivated 'Base1: External TRIG In' Trigger signal from TRIG IN connector 'AFRF Gen1: ...' Trigger signal from processed waveform file
		"""
		response = self._core.io.query_str('TRIGger:BASE:OUT:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:BASE:OUT:SOURce \n
		Snippet: driver.trigger.base.out.set_source(source = '1') \n
		Selects the output trigger signal to be routed to the TRIG OUT connector. \n
			:param source: Source as string, examples: 'No Connection' TRIG OUT connector deactivated 'Base1: External TRIG In' Trigger signal from TRIG IN connector 'AFRF Gen1: ...' Trigger signal from processed waveform file
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:BASE:OUT:SOURce {param}')

	def clone(self) -> 'Out':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Out(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
