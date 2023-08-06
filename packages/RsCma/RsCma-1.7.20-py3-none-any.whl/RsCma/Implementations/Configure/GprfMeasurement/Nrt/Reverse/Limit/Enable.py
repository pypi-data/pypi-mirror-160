from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, power: bool, return_loss: bool, reflection: bool, swr: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:ENABle \n
		Snippet: driver.configure.gprfMeasurement.nrt.reverse.limit.enable.set(power = False, return_loss = False, reflection = False, swr = False) \n
		Enables/disables the limit check for the reverse direction results. \n
			:param power: OFF | ON
			:param return_loss: OFF | ON
			:param reflection: OFF | ON
			:param swr: OFF | ON
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('power', power, DataType.Boolean), ArgSingle('return_loss', return_loss, DataType.Boolean), ArgSingle('reflection', reflection, DataType.Boolean), ArgSingle('swr', swr, DataType.Boolean))
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:ENABle {param}'.rstrip())

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Response structure. Fields: \n
			- Power: bool: OFF | ON
			- Return_Loss: bool: OFF | ON
			- Reflection: bool: OFF | ON
			- Swr: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Power'),
			ArgStruct.scalar_bool('Return_Loss'),
			ArgStruct.scalar_bool('Reflection'),
			ArgStruct.scalar_bool('Swr')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Power: bool = None
			self.Return_Loss: bool = None
			self.Reflection: bool = None
			self.Swr: bool = None

	def get(self) -> EnableStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:ENABle \n
		Snippet: value: EnableStruct = driver.configure.gprfMeasurement.nrt.reverse.limit.enable.get() \n
		Enables/disables the limit check for the reverse direction results. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:ENABle?', self.__class__.EnableStruct())
