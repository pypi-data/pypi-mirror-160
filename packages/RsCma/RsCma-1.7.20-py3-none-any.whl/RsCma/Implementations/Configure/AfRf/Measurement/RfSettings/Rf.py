from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rf:
	"""Rf commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rf", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:RF:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.rfSettings.rf.get_enable() \n
		Enables or disables the RF input path. \n
			:return: rf_enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:RFSettings:RF:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, rf_enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:RFSettings:RF:ENABle \n
		Snippet: driver.configure.afRf.measurement.rfSettings.rf.set_enable(rf_enable = False) \n
		Enables or disables the RF input path. \n
			:param rf_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(rf_enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:RFSettings:RF:ENABle {param}')
