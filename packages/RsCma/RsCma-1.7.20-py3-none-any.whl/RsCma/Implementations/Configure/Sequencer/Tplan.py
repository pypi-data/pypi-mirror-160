from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tplan:
	"""Tplan commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tplan", core, parent)

	def run(self, test_plan_name: str) -> None:
		"""SCPI: CONFigure:SEQuencer:TPLan:RUN \n
		Snippet: driver.configure.sequencer.tplan.run(test_plan_name = '1') \n
		No command help available \n
			:param test_plan_name: No help available
		"""
		param = Conversions.value_to_quoted_str(test_plan_name)
		self._core.io.write(f'CONFigure:SEQuencer:TPLan:RUN {param}')

	def abort(self, test_plan_name: str) -> None:
		"""SCPI: CONFigure:SEQuencer:TPLan:ABORt \n
		Snippet: driver.configure.sequencer.tplan.abort(test_plan_name = '1') \n
		No command help available \n
			:param test_plan_name: No help available
		"""
		param = Conversions.value_to_quoted_str(test_plan_name)
		self._core.io.write(f'CONFigure:SEQuencer:TPLan:ABORt {param}')
