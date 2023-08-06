from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class External:
	"""External commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("external", core, parent)

	# noinspection PyTypeChecker
	def get_li_range(self) -> enums.LockRangeExternal:
		"""SCPI: SYSTem:BASE:REFerence:EXTernal:LIRange \n
		Snippet: value: enums.LockRangeExternal = driver.system.base.reference.external.get_li_range() \n
		Selects the width of the lock-in range, used to synchronize to an external reference frequency source. \n
			:return: li_range: WIDE | MEDium | NARRow | INV INV means that the source is unusable, for example because of an ongoing adjustment
		"""
		response = self._core.io.query_str_with_opc('SYSTem:BASE:REFerence:EXTernal:LIRange?')
		return Conversions.str_to_scalar_enum(response, enums.LockRangeExternal)

	def set_li_range(self, li_range: enums.LockRangeExternal) -> None:
		"""SCPI: SYSTem:BASE:REFerence:EXTernal:LIRange \n
		Snippet: driver.system.base.reference.external.set_li_range(li_range = enums.LockRangeExternal.INV) \n
		Selects the width of the lock-in range, used to synchronize to an external reference frequency source. \n
			:param li_range: WIDE | MEDium | NARRow | INV INV means that the source is unusable, for example because of an ongoing adjustment
		"""
		param = Conversions.enum_scalar_to_str(li_range, enums.LockRangeExternal)
		self._core.io.write_with_opc(f'SYSTem:BASE:REFerence:EXTernal:LIRange {param}')
