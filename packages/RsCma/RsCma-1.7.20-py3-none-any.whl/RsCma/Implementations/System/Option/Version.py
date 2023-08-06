from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.Utilities import trim_str_response
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Version:
	"""Version commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("version", core, parent)

	def get(self, applicname: str = None) -> str:
		"""SCPI: SYSTem:OPTion:VERSion \n
		Snippet: value: str = driver.system.option.version.get(applicname = '1') \n
		Returns version information for installed software packages.
			INTRO_CMD_HELP: The structure of the returned string depends on the parameter <Application>: \n
			- If <Application> is specified Returned string: '<Version>' '0' means that the application is unknown or not installed.
			- If <Application> is omitted Returned string: '<PackageName1>,<Version1>;<PackageName2>,<Version2>;...' \n
			:param applicname: No help available
			:return: option_list: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('applicname', applicname, DataType.String, None, is_optional=True))
		response = self._core.io.query_str(f'SYSTem:OPTion:VERSion? {param}'.rstrip())
		return trim_str_response(response)
