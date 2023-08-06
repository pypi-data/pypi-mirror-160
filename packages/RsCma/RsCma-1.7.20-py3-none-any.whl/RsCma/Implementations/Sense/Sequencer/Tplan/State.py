from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	# noinspection PyTypeChecker
	def get(self, tp_name: str) -> enums.TestPlanState:
		"""SCPI: SENSe:SEQuencer:TPLan:STATe \n
		Snippet: value: enums.TestPlanState = driver.sense.sequencer.tplan.state.get(tp_name = '1') \n
		No command help available \n
			:param tp_name: No help available
			:return: state: No help available"""
		param = Conversions.value_to_quoted_str(tp_name)
		response = self._core.io.query_str(f'SENSe:SEQuencer:TPLan:STATe? {param}')
		return Conversions.str_to_scalar_enum(response, enums.TestPlanState)
