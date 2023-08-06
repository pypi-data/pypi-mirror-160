from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Second:
	"""Second commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("second", core, parent)

	def get_mlevel(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AIN:SECond:MLEVel \n
		Snippet: value: float = driver.source.afRf.generator.audioInput.second.get_mlevel() \n
		Specifies the maximum expected level for the AF2 IN connector. This setting is only relevant, if auto ranging is disabled. \n
			:return: level: Maximum expected level Range: 10E-6 V to 43 V, Unit: V
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:AIN:SECond:MLEVel?')
		return Conversions.str_to_float(response)

	def set_mlevel(self, level: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:AIN:SECond:MLEVel \n
		Snippet: driver.source.afRf.generator.audioInput.second.set_mlevel(level = 1.0) \n
		Specifies the maximum expected level for the AF2 IN connector. This setting is only relevant, if auto ranging is disabled. \n
			:param level: Maximum expected level Range: 10E-6 V to 43 V, Unit: V
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:AIN:SECond:MLEVel {param}')
