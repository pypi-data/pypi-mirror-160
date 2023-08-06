from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sout:
	"""Sout commands group definition. 4 total commands, 3 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sout", core, parent)

	@property
	def delay(self):
		"""delay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_delay'):
			from .Delay import Delay
			self._delay = Delay(self._core, self._cmd_group)
		return self._delay

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Level import Level
			self._level = Level(self._core, self._cmd_group)
		return self._level

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import Enable
			self._enable = Enable(self._core, self._cmd_group)
		return self._enable

	def set(self, source_left: enums.SignalSource, source_right: enums.SignalSource) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT \n
		Snippet: driver.source.afRf.generator.sout.set(source_left = enums.SignalSource.AFI1, source_right = enums.SignalSource.AFI1) \n
		Selects audio signal sources for the left and right channel of the SPDIF OUT connector. \n
			:param source_left: GEN3 | AFI1 | SPIL GEN3 Audio generator 3 AFI1 AF1 IN SPIL SPDIF IN, left channel
			:param source_right: GEN4 | AFI2 | SPIR GEN4 Audio generator 4 AFI2 AF2 IN SPIR SPDIF IN, right channel
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('source_left', source_left, DataType.Enum, enums.SignalSource), ArgSingle('source_right', source_right, DataType.Enum, enums.SignalSource))
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:SOUT {param}'.rstrip())

	# noinspection PyTypeChecker
	class SoutStruct(StructBase):
		"""Response structure. Fields: \n
			- Source_Left: enums.SignalSource: GEN3 | AFI1 | SPIL GEN3 Audio generator 3 AFI1 AF1 IN SPIL SPDIF IN, left channel
			- Source_Right: enums.SignalSource: GEN4 | AFI2 | SPIR GEN4 Audio generator 4 AFI2 AF2 IN SPIR SPDIF IN, right channel"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Source_Left', enums.SignalSource),
			ArgStruct.scalar_enum('Source_Right', enums.SignalSource)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Source_Left: enums.SignalSource = None
			self.Source_Right: enums.SignalSource = None

	def get(self) -> SoutStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:SOUT \n
		Snippet: value: SoutStruct = driver.source.afRf.generator.sout.get() \n
		Selects audio signal sources for the left and right channel of the SPDIF OUT connector. \n
			:return: structure: for return value, see the help for SoutStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:AFRF:GENerator<Instance>:SOUT?', self.__class__.SoutStruct())

	def clone(self) -> 'Sout':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sout(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
