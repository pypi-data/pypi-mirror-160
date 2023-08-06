from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Internal:
	"""Internal commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("internal", core, parent)

	# noinspection PyTypeChecker
	def get_li_range(self) -> enums.LockRangeInternal:
		"""SCPI: SYSTem:BASE:REFerence:INTernal:LIRange \n
		Snippet: value: enums.LockRangeInternal = driver.system.base.reference.internal.get_li_range() \n
		Selects the type of an internal reference frequency source. \n
			:return: li_range: MEDium | NARRow | INV MEDium TCXO NARRow OCXO INV Source unusable, for example adjustment ongoing
		"""
		response = self._core.io.query_str_with_opc('SYSTem:BASE:REFerence:INTernal:LIRange?')
		return Conversions.str_to_scalar_enum(response, enums.LockRangeInternal)

	def set_li_range(self, li_range: enums.LockRangeInternal) -> None:
		"""SCPI: SYSTem:BASE:REFerence:INTernal:LIRange \n
		Snippet: driver.system.base.reference.internal.set_li_range(li_range = enums.LockRangeInternal.INV) \n
		Selects the type of an internal reference frequency source. \n
			:param li_range: MEDium | NARRow | INV MEDium TCXO NARRow OCXO INV Source unusable, for example adjustment ongoing
		"""
		param = Conversions.enum_scalar_to_str(li_range, enums.LockRangeInternal)
		self._core.io.write_with_opc(f'SYSTem:BASE:REFerence:INTernal:LIRange {param}')
