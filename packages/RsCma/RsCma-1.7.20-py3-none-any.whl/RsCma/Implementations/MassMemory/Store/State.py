from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("state", core, parent)

	def set(self, sav_rcl_state_number: int, filename: str, msus: str = None) -> None:
		"""SCPI: MMEMory:STORe:STATe \n
		Snippet: driver.massMemory.store.state.set(sav_rcl_state_number = 1, filename = '1', msus = '1') \n
		Stores the instrument settings from the specified internal memory to the specified file. To store the current instrument
		settings to the memory, use *SAV <MemoryNumber> first. \n
			:param sav_rcl_state_number: No help available
			:param filename: No help available
			:param msus: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('sav_rcl_state_number', sav_rcl_state_number, DataType.Integer), ArgSingle('filename', filename, DataType.String), ArgSingle('msus', msus, DataType.String, None, is_optional=True))
		self._core.io.write(f'MMEMory:STORe:STATe {param}'.rstrip())
