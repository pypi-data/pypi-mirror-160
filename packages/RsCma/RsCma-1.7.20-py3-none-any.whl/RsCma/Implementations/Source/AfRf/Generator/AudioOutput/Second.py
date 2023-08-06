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
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AOUT:SECond:LEVel \n
		Snippet: value: float = driver.source.afRf.generator.audioOutput.second.get_level() \n
		Specifies the output level for the AF2 OUT connector. For noise signals provided by an internal generator, the maximum
		allowed level is reduced by the factor 1/sqrt(2) . \n
			:return: level: Output level Range: 10E-6 V to 5 V, Unit: V
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:AOUT:SECond:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AOUT:SECond:LEVel \n
		Snippet: driver.source.afRf.generator.audioOutput.second.set_level(level = 1.0) \n
		Specifies the output level for the AF2 OUT connector. For noise signals provided by an internal generator, the maximum
		allowed level is reduced by the factor 1/sqrt(2) . \n
			:param level: Output level Range: 10E-6 V to 5 V, Unit: V
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:AOUT:SECond:LEVel {param}')
