from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Digital:
	"""Digital commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("digital", core, parent)

	def get_file(self) -> str:
		"""SCPI: SOURce:XRT:GENerator<Instance>:DIGital:FILE \n
		Snippet: value: str = driver.source.xrt.generator.digital.get_file() \n
		No command help available \n
			:return: arb_file: No help available
		"""
		response = self._core.io.query_str_with_opc('SOURce:XRT:GENerator<Instance>:DIGital:FILE?')
		return trim_str_response(response)

	def set_file(self, arb_file: str) -> None:
		"""SCPI: SOURce:XRT:GENerator<Instance>:DIGital:FILE \n
		Snippet: driver.source.xrt.generator.digital.set_file(arb_file = '1') \n
		No command help available \n
			:param arb_file: No help available
		"""
		param = Conversions.value_to_quoted_str(arb_file)
		self._core.io.write_with_opc(f'SOURce:XRT:GENerator<Instance>:DIGital:FILE {param}')
