from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("time", core, parent)

	@property
	def tzone(self):
		"""tzone commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tzone'):
			from .Tzone import Tzone
			self._tzone = Tzone(self._core, self._cmd_group)
		return self._tzone

	def set(self, hour: int, min_py: int, sec: int) -> None:
		"""SCPI: SYSTem:BASE:TIME \n
		Snippet: driver.system.base.time.set(hour = 1, min_py = 1, sec = 1) \n
		No command help available \n
			:param hour: No help available
			:param min_py: No help available
			:param sec: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('hour', hour, DataType.Integer), ArgSingle('min_py', min_py, DataType.Integer), ArgSingle('sec', sec, DataType.Integer))
		self._core.io.write(f'SYSTem:BASE:TIME {param}'.rstrip())

	# noinspection PyTypeChecker
	class TimeStruct(StructBase):
		"""Response structure. Fields: \n
			- Hour: int: No parameter help available
			- Min_Py: int: No parameter help available
			- Sec: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Hour'),
			ArgStruct.scalar_int('Min_Py'),
			ArgStruct.scalar_int('Sec')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Hour: int = None
			self.Min_Py: int = None
			self.Sec: int = None

	def get(self) -> TimeStruct:
		"""SCPI: SYSTem:BASE:TIME \n
		Snippet: value: TimeStruct = driver.system.base.time.get() \n
		No command help available \n
			:return: structure: for return value, see the help for TimeStruct structure arguments."""
		return self._core.io.query_struct(f'SYSTem:BASE:TIME?', self.__class__.TimeStruct())

	def clone(self) -> 'Time':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Time(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
