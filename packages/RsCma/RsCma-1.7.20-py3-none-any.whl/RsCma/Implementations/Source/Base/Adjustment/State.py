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

	def set(self, control: bool) -> None:
		"""SCPI: SOURce:BASE:ADJustment:STATe \n
		Snippet: driver.source.base.adjustment.state.set(control = False) \n
		Starts or terminates the adjustment of the reference frequency. A query returns the current state. \n
			:param control: ON | OFF ON Starts the adjustment OFF Terminates the adjustment
		"""
		param = Conversions.bool_to_str(control)
		self._core.io.write_with_opc(f'SOURce:BASE:ADJustment:STATe {param}')

	# noinspection PyTypeChecker
	def get(self) -> enums.GeneratorState:
		"""SCPI: SOURce:BASE:ADJustment:STATe \n
		Snippet: value: enums.GeneratorState = driver.source.base.adjustment.state.get() \n
		Starts or terminates the adjustment of the reference frequency. A query returns the current state. \n
			:return: state: OFF | PENDing | ON OFF No adjustment in progress PENDing State transition ongoing ON Adjustment in progress"""
		response = self._core.io.query_str_with_opc(f'SOURce:BASE:ADJustment:STATe?')
		return Conversions.str_to_scalar_enum(response, enums.GeneratorState)
