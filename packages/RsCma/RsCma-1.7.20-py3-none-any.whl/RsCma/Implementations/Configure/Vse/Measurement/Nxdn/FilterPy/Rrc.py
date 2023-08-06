from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rrc:
	"""Rrc commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rrc", core, parent)

	def get_roff_factor(self) -> float:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:NXDN:FILTer:RRC:ROFFfactor \n
		Snippet: value: float = driver.configure.vse.measurement.nxdn.filterPy.rrc.get_roff_factor() \n
		Queries the roll-off factor of the filter used for pulse shaping for NXDN. \n
			:return: rolloff_factor: No help available
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:NXDN:FILTer:RRC:ROFFfactor?')
		return Conversions.str_to_float(response)
