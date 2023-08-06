from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Custom:
	"""Custom commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("custom", core, parent)

	def get_load(self) -> str:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:CUSTom:LOAD \n
		Snippet: value: str = driver.configure.vse.measurement.custom.get_load() \n
		Loads a VSE recall file with file extension *.dfl. You can load VSE recall files from the data directory of the internal
		storage medium (D:/Rohde-Schwarz/CMA/Data or subfolder) or from a USB storage medium. \n
			:return: filename: No help available
		"""
		response = self._core.io.query_str('CONFigure:VSE:MEASurement<Instance>:CUSTom:LOAD?')
		return trim_str_response(response)

	def set_load(self, filename: str) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:CUSTom:LOAD \n
		Snippet: driver.configure.vse.measurement.custom.set_load(filename = '1') \n
		Loads a VSE recall file with file extension *.dfl. You can load VSE recall files from the data directory of the internal
		storage medium (D:/Rohde-Schwarz/CMA/Data or subfolder) or from a USB storage medium. \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:CUSTom:LOAD {param}')

	def save(self, filename: str) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:CUSTom:SAVE \n
		Snippet: driver.configure.vse.measurement.custom.save(filename = '1') \n
		Saves a VSE recall file with file extension *.dfl. You can save VSE recall files to the data directory of the internal
		storage medium (D:/Rohde-Schwarz/CMA/Data or subfolder) or to a USB storage medium. \n
			:param filename: No help available
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:CUSTom:SAVE {param}')
