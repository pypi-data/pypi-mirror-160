from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ttime:
	"""Ttime commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ttime", core, parent)

	def get_first(self) -> float:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SCAL:TTIMe:FIRSt \n
		Snippet: value: float = driver.source.afRf.generator.dialing.scal.ttime.get_first() \n
		Defines the duration of a dual tone of a SELCAL sequence. \n
			:return: ttime: Range: 0.2 s to 3 s, Unit: s
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:SCAL:TTIMe:FIRSt?')
		return Conversions.str_to_float(response)

	def set_first(self, ttime: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:SCAL:TTIMe:FIRSt \n
		Snippet: driver.source.afRf.generator.dialing.scal.ttime.set_first(ttime = 1.0) \n
		Defines the duration of a dual tone of a SELCAL sequence. \n
			:param ttime: Range: 0.2 s to 3 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(ttime)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:SCAL:TTIMe:FIRSt {param}')
