from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Estatus:
	"""Estatus commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("estatus", core, parent)

	# noinspection PyTypeChecker
	def get(self, tp_name: str) -> enums.Status:
		"""SCPI: SENSe:SEQuencer:TPLan:ESTatus \n
		Snippet: value: enums.Status = driver.sense.sequencer.tplan.estatus.get(tp_name = '1') \n
		No command help available \n
			:param tp_name: No help available
			:return: status: No help available"""
		param = Conversions.value_to_quoted_str(tp_name)
		response = self._core.io.query_str(f'SENSe:SEQuencer:TPLan:ESTatus? {param}')
		return Conversions.str_to_scalar_enum(response, enums.Status)
