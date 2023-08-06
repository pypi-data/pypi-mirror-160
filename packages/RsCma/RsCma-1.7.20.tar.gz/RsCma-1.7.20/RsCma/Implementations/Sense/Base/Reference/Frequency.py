from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def get_locked(self) -> bool:
		"""SCPI: SENSe:BASE:REFerence:FREQuency:LOCKed \n
		Snippet: value: bool = driver.sense.base.reference.frequency.get_locked() \n
		Queries whether the reference frequency is locked or not. \n
			:return: lock: 1 | 0 1: Frequency is locked 0: Frequency is not locked
		"""
		response = self._core.io.query_str('SENSe:BASE:REFerence:FREQuency:LOCKed?')
		return Conversions.str_to_bool(response)

	def get_oven_cold(self) -> bool:
		"""SCPI: SENSe:BASE:REFerence:FREQuency:OVENcold \n
		Snippet: value: bool = driver.sense.base.reference.frequency.get_oven_cold() \n
		Queries whether an installed OCXO has completed the warm-up phase and has reached its operating temperature. \n
			:return: oven_cold: 0 | 1 0: warm-up completed, operating temperature reached 1: oven still cold, warm-up is ongoing
		"""
		response = self._core.io.query_str('SENSe:BASE:REFerence:FREQuency:OVENcold?')
		return Conversions.str_to_bool(response)
