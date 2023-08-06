from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Code:
	"""Code commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("code", core, parent)

	def get_all(self) -> int:
		"""SCPI: SYSTem:ERRor:CODE:ALL \n
		Snippet: value: int = driver.system.error.code.get_all() \n
		Queries the error code numbers of all entries in the error queue and deletes all entries. \n
			:return: error_code: Comma-separated list of error codes 0 means that the queue is empty. Positive error codes are instrument-dependent. Negative error codes are reserved by the SCPI standard.
		"""
		response = self._core.io.query_str('SYSTem:ERRor:CODE:ALL?')
		return Conversions.str_to_int(response)

	def get_next(self) -> int:
		"""SCPI: SYSTem:ERRor:CODE[:NEXT] \n
		Snippet: value: int = driver.system.error.code.get_next() \n
		Queries the code number of the oldest entry in the error queue and deletes the entry. \n
			:return: error: 0 means that the queue is empty. Positive error codes are instrument-dependent. Negative error codes are reserved by the SCPI standard.
		"""
		response = self._core.io.query_str('SYSTem:ERRor:CODE:NEXT?')
		return Conversions.str_to_int(response)
