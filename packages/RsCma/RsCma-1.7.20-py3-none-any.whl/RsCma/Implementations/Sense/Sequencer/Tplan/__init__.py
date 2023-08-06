from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tplan:
	"""Tplan commands group definition. 4 total commands, 2 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tplan", core, parent)

	@property
	def state(self):
		"""state commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .State import State
			self._state = State(self._core, self._cmd_group)
		return self._state

	@property
	def estatus(self):
		"""estatus commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_estatus'):
			from .Estatus import Estatus
			self._estatus = Estatus(self._core, self._cmd_group)
		return self._estatus

	def get_list_py(self) -> List[str]:
		"""SCPI: SENSe:SEQuencer:TPLan:LIST \n
		Snippet: value: List[str] = driver.sense.sequencer.tplan.get_list_py() \n
		No command help available \n
			:return: tp_list: No help available
		"""
		response = self._core.io.query_str('SENSe:SEQuencer:TPLan:LIST?')
		return Conversions.str_to_str_list(response)

	# noinspection PyTypeChecker
	class InfoStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Tp_Name: List[str]: No parameter help available
			- State: List[enums.TestPlanState]: No parameter help available
			- Status: List[enums.Status]: No parameter help available"""
		__meta_args_list = [
			ArgStruct('Tp_Name', DataType.StringList, None, False, True, 1),
			ArgStruct('State', DataType.EnumList, enums.TestPlanState, False, True, 1),
			ArgStruct('Status', DataType.EnumList, enums.Status, False, True, 1)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Tp_Name: List[str] = None
			self.State: List[enums.TestPlanState] = None
			self.Status: List[enums.Status] = None

	def get_info(self) -> InfoStruct:
		"""SCPI: SENSe:SEQuencer:TPLan:INFO \n
		Snippet: value: InfoStruct = driver.sense.sequencer.tplan.get_info() \n
		No command help available \n
			:return: structure: for return value, see the help for InfoStruct structure arguments.
		"""
		return self._core.io.query_struct('SENSe:SEQuencer:TPLan:INFO?', self.__class__.InfoStruct())

	def clone(self) -> 'Tplan':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tplan(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
