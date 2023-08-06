from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("file", core, parent)

	def get_date(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:FILE:DATE \n
		Snippet: value: str = driver.source.afRf.generator.arb.file.get_date() \n
		Queries the date and time of the loaded ARB file. \n
			:return: date: String with date and time
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:FILE:DATE?')
		return trim_str_response(response)

	def get_option(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:FILE:OPTion \n
		Snippet: value: str = driver.source.afRf.generator.arb.file.get_option() \n
		Queries the options that are required to process the loaded ARB file. \n
			:return: options: String with comma-separated list of options
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:FILE:OPTion?')
		return trim_str_response(response)

	def get_version(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:FILE:VERSion \n
		Snippet: value: str = driver.source.afRf.generator.arb.file.get_version() \n
		Queries the version of the loaded ARB file. \n
			:return: version: String containing the version Empty string, if no file version is defined
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:FILE:VERSion?')
		return trim_str_response(response)

	def get_value(self) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:FILE \n
		Snippet: value: str = driver.source.afRf.generator.arb.file.get_value() \n
		Selects the ARB file to be processed. Specify the path and the filename. If the file is stored in the folder
		corresponding to the @waveform alias, it is sufficient to specify only the filename.
			INTRO_CMD_HELP: Example, the following strings are equivalent: \n
			- 'D:/Rohde-Schwarz/CMA/Data/waveform/myfile.wv'
			- '@WAVEFORM/myfile.wv'
			- 'myfile.wv' \n
			:return: arb_file: String specifying the ARB file
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:ARB:FILE?')
		return trim_str_response(response)

	def set_value(self, arb_file: str) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:FILE \n
		Snippet: driver.source.afRf.generator.arb.file.set_value(arb_file = '1') \n
		Selects the ARB file to be processed. Specify the path and the filename. If the file is stored in the folder
		corresponding to the @waveform alias, it is sufficient to specify only the filename.
			INTRO_CMD_HELP: Example, the following strings are equivalent: \n
			- 'D:/Rohde-Schwarz/CMA/Data/waveform/myfile.wv'
			- '@WAVEFORM/myfile.wv'
			- 'myfile.wv' \n
			:param arb_file: String specifying the ARB file
		"""
		param = Conversions.value_to_quoted_str(arb_file)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:ARB:FILE {param}')
