from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Notch:
	"""Notch commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("notch", core, parent)

	# noinspection PyTypeChecker
	def get_path(self) -> enums.NotchPath:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FILTer:NOTCh:PATH \n
		Snippet: value: enums.NotchPath = driver.configure.afRf.measurement.filterPy.notch.get_path() \n
		Selects the active path for the notch filters in the 'AF IN', 'SPDIF IN' and 'VoIP' subtabs. \n
			:return: path: AF | SPDIF | VoIP
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:FILTer:NOTCh:PATH?')
		return Conversions.str_to_scalar_enum(response, enums.NotchPath)

	def set_path(self, path: enums.NotchPath) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:FILTer:NOTCh:PATH \n
		Snippet: driver.configure.afRf.measurement.filterPy.notch.set_path(path = enums.NotchPath.AF) \n
		Selects the active path for the notch filters in the 'AF IN', 'SPDIF IN' and 'VoIP' subtabs. \n
			:param path: AF | SPDIF | VoIP
		"""
		param = Conversions.enum_scalar_to_str(path, enums.NotchPath)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:FILTer:NOTCh:PATH {param}')
