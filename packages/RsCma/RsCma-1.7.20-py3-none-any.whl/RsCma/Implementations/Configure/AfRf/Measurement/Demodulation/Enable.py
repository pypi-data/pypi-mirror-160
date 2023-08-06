from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, test_left: bool, test_right: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:ENABle \n
		Snippet: driver.configure.afRf.measurement.demodulation.enable.set(test_left = False, test_right = False) \n
		No command help available \n
			:param test_left: No help available
			:param test_right: No help available
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('test_left', test_left, DataType.Boolean), ArgSingle('test_right', test_right, DataType.Boolean))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:ENABle {param}'.rstrip())

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Response structure. Fields: \n
			- Test_Left: bool: No parameter help available
			- Test_Right: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Test_Left'),
			ArgStruct.scalar_bool('Test_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Test_Left: bool = None
			self.Test_Right: bool = None

	def get(self) -> EnableStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:ENABle \n
		Snippet: value: EnableStruct = driver.configure.afRf.measurement.demodulation.enable.get() \n
		No command help available \n
			:return: structure: for return value, see the help for EnableStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:ENABle?', self.__class__.EnableStruct())
