from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ada:
	"""Ada commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ada", core, parent)

	def get_arm(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:ADA:ARM \n
		Snippet: value: bool = driver.configure.afRf.measurement.ada.get_arm() \n
		No command help available \n
			:return: arm: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:ADA:ARM?')
		return Conversions.str_to_bool(response)

	def set_arm(self, arm: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:ADA:ARM \n
		Snippet: driver.configure.afRf.measurement.ada.set_arm(arm = False) \n
		No command help available \n
			:param arm: No help available
		"""
		param = Conversions.bool_to_str(arm)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:ADA:ARM {param}')
