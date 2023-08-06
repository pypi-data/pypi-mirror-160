from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Second:
	"""Second commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("second", core, parent)

	def get_level(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AOUT:SECond:LEVel \n
		Snippet: value: float = driver.configure.afRf.measurement.audioOutput.second.get_level() \n
		Specifies the output level for the AF2 OUT connector. Use this command, if you want to set different level units, e.g.
		dBm (Table 'Units relevant for remote commands') , or set the level for both connectors independently. \n
			:return: level: Range: 10E-6 V to 5 V, Unit: V
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:AOUT:SECond:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AOUT:SECond:LEVel \n
		Snippet: driver.configure.afRf.measurement.audioOutput.second.set_level(level = 1.0) \n
		Specifies the output level for the AF2 OUT connector. Use this command, if you want to set different level units, e.g.
		dBm (Table 'Units relevant for remote commands') , or set the level for both connectors independently. \n
			:param level: Range: 10E-6 V to 5 V, Unit: V
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AOUT:SECond:LEVel {param}')
