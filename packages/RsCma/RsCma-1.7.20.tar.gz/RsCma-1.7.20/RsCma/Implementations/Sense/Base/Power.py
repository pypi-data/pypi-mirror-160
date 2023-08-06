from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Power:
	"""Power commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("power", core, parent)

	# noinspection PyTypeChecker
	def get_omode(self) -> enums.SupplyMode:
		"""SCPI: SENSe:BASE:POWer:OMODe \n
		Snippet: value: enums.SupplyMode = driver.sense.base.power.get_omode() \n
		Queries whether the instrument is powered by an inserted battery or by an external power supply. \n
			:return: oper_mode: BATTery | MAINs
		"""
		response = self._core.io.query_str('SENSe:BASE:POWer:OMODe?')
		return Conversions.str_to_scalar_enum(response, enums.SupplyMode)
