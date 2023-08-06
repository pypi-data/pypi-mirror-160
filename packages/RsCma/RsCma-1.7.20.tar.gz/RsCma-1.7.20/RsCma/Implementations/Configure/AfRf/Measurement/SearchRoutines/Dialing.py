from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dialing:
	"""Dialing commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dialing", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:DIALing:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.searchRoutines.dialing.get_enable() \n
		Enables the dialing of a tone sequence before the first measurement of the search routine. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:DIALing:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:DIALing:ENABle \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.dialing.set_enable(enable = False) \n
		Enables the dialing of a tone sequence before the first measurement of the search routine. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:DIALing:ENABle {param}')
