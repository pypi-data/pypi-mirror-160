from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delay", core, parent)

	def set(self, enable_left: bool, enable_right: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT:DELay \n
		Snippet: driver.source.afRf.generator.sout.delay.set(enable_left = False, enable_right = False) \n
		No command help available \n
			:param enable_left: No help available
			:param enable_right: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable_left', enable_left, DataType.Boolean), ArgSingle('enable_right', enable_right, DataType.Boolean))
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:SOUT:DELay {param}'.rstrip())

	# noinspection PyTypeChecker
	class DelayStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable_Left: bool: No parameter help available
			- Enable_Right: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_bool('Enable_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Enable_Right: bool = None

	def get(self) -> DelayStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT:DELay \n
		Snippet: value: DelayStruct = driver.source.afRf.generator.sout.delay.get() \n
		No command help available \n
			:return: structure: for return value, see the help for DelayStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:AFRF:GENerator<Instance>:SOUT:DELay?', self.__class__.DelayStruct())
