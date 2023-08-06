from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Item:
	"""Item commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("item", core, parent)

	def set(self, item_path: str, filename: str) -> None:
		"""SCPI: MMEMory:LOAD:ITEM \n
		Snippet: driver.massMemory.load.item.set(item_path = '1', filename = '1') \n
		No command help available \n
			:param item_path: No help available
			:param filename: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('item_path', item_path, DataType.String), ArgSingle('filename', filename, DataType.String))
		self._core.io.write(f'MMEMory:LOAD:ITEM {param}'.rstrip())
