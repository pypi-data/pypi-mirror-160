from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Length:
	"""Length commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("length", core, parent)

	def get(self, path_name: str = None) -> int:
		"""SCPI: MMEMory:DCATalog:LENGth \n
		Snippet: value: int = driver.massMemory.dcatalog.length.get(path_name = '1') \n
		Returns the number of subdirectories of the specified directory. The number corresponds to the number of strings returned
		by the method RsCma.MassMemory.Dcatalog.get_ command. \n
			:param path_name: String parameter to specify the directory. If the parameter is omitted, the command queries the contents of the current directory (see method RsCma.MassMemory.CurrentDirectory.set) . If the wildcards ? or * are used, the number of subdirectories matching this pattern are returned.
			:return: file_entry_count: No help available"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('path_name', path_name, DataType.String, None, is_optional=True))
		response = self._core.io.query_str(f'MMEMory:DCATalog:LENGth? {param}'.rstrip())
		return Conversions.str_to_int(response)
