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

	def set(self, enable_left: bool, enable_right: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SOUT:ENABle \n
		Snippet: driver.configure.afRf.measurement.sout.enable.set(enable_left = False, enable_right = False) \n
		Enables or disables the channels of the SPDIF OUT connector. \n
			:param enable_left: OFF | ON Switches the left channel off or on
			:param enable_right: OFF | ON Switches the right channel off or on
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable_left', enable_left, DataType.Boolean), ArgSingle('enable_right', enable_right, DataType.Boolean))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SOUT:ENABle {param}'.rstrip())

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable_Left: bool: OFF | ON Switches the left channel off or on
			- Enable_Right: bool: OFF | ON Switches the right channel off or on"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_bool('Enable_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Enable_Right: bool = None

	def get(self) -> EnableStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SOUT:ENABle \n
		Snippet: value: EnableStruct = driver.configure.afRf.measurement.sout.enable.get() \n
		Enables or disables the channels of the SPDIF OUT connector. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SOUT:ENABle?', self.__class__.EnableStruct())
