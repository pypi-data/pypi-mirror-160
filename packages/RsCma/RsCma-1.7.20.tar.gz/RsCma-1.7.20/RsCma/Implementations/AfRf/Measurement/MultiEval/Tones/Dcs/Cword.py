from typing import List

from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .......Internal.Types import DataType


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cword:
	"""Cword commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cword", core, parent)

	def fetch(self) -> List[str]:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:CWORd \n
		Snippet: value: List[str] = driver.afRf.measurement.multiEval.tones.dcs.cword.fetch() \n
		No command help available \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: codeword: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'FETCh:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:CWORd?', suppressed)
		return Conversions.str_to_str_list(response)

	def read(self) -> List[str]:
		"""SCPI: READ:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:CWORd \n
		Snippet: value: List[str] = driver.afRf.measurement.multiEval.tones.dcs.cword.read() \n
		No command help available \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:return: codeword: No help available"""
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'READ:AFRF:MEASurement<Instance>:MEValuation:TONes:DCS:CWORd?', suppressed)
		return Conversions.str_to_str_list(response)
