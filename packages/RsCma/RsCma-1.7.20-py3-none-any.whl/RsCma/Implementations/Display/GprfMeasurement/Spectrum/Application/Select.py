from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("select", core, parent)

	def set(self, application: enums.SpecAnApp, fullscreen: bool = None) -> None:
		"""SCPI: DISPlay:GPRF:MEASurement<Instance>:SPECtrum:APPLication:SELect \n
		Snippet: driver.display.gprfMeasurement.spectrum.application.select.set(application = enums.SpecAnApp.FREQ, fullscreen = False) \n
		Configures the display of the 'Spectrum Analyzer' tab. \n
			:param application: FREQ | ZERO Show 'Frequency Sweep' subtab or 'Zero Span' subtab
			:param fullscreen: OFF | ON OFF: show result diagram with default size ON: maximize result diagram
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('application', application, DataType.Enum, enums.SpecAnApp), ArgSingle('fullscreen', fullscreen, DataType.Boolean, None, is_optional=True))
		self._core.io.write(f'DISPlay:GPRF:MEASurement<Instance>:SPECtrum:APPLication:SELect {param}'.rstrip())

	# noinspection PyTypeChecker
	class SelectStruct(StructBase):
		"""Response structure. Fields: \n
			- Application: enums.SpecAnApp: FREQ | ZERO Show 'Frequency Sweep' subtab or 'Zero Span' subtab
			- Fullscreen: bool: OFF | ON OFF: show result diagram with default size ON: maximize result diagram"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Application', enums.SpecAnApp),
			ArgStruct.scalar_bool('Fullscreen')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Application: enums.SpecAnApp = None
			self.Fullscreen: bool = None

	def get(self) -> SelectStruct:
		"""SCPI: DISPlay:GPRF:MEASurement<Instance>:SPECtrum:APPLication:SELect \n
		Snippet: value: SelectStruct = driver.display.gprfMeasurement.spectrum.application.select.get() \n
		Configures the display of the 'Spectrum Analyzer' tab. \n
			:return: structure: for return value, see the help for SelectStruct structure arguments."""
		return self._core.io.query_struct(f'DISPlay:GPRF:MEASurement<Instance>:SPECtrum:APPLication:SELect?', self.__class__.SelectStruct())
