from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delays:
	"""Delays commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delays", core, parent)

	def set(self, marker_2: int, marker_3: int, marker_4: int, restart_marker: int) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:MARKer:DELays \n
		Snippet: driver.source.afRf.generator.arb.marker.delays.set(marker_2 = 1, marker_3 = 1, marker_4 = 1, restart_marker = 1) \n
		Defines delay times for the generation of trigger signals relative to the marker events. All delay times are specified as
		number of samples. \n
			:param marker_2: Delay for marker 2 of the ARB file Range: -10 to 4000
			:param marker_3: Delay for marker 3 of the ARB file Range: -10 to 4000
			:param marker_4: Delay for marker 4 of the ARB file Range: -10 to 4000
			:param restart_marker: Delay for marker event due to start of ARB file processing Range: 0 to n (depends on ARB file)
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('marker_2', marker_2, DataType.Integer), ArgSingle('marker_3', marker_3, DataType.Integer), ArgSingle('marker_4', marker_4, DataType.Integer), ArgSingle('restart_marker', restart_marker, DataType.Integer))
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:ARB:MARKer:DELays {param}'.rstrip())

	# noinspection PyTypeChecker
	class DelaysStruct(StructBase):
		"""Response structure. Fields: \n
			- Marker_2: int: Delay for marker 2 of the ARB file Range: -10 to 4000
			- Marker_3: int: Delay for marker 3 of the ARB file Range: -10 to 4000
			- Marker_4: int: Delay for marker 4 of the ARB file Range: -10 to 4000
			- Restart_Marker: int: Delay for marker event due to start of ARB file processing Range: 0 to n (depends on ARB file)"""
		__meta_args_list = [
			ArgStruct.scalar_int('Marker_2'),
			ArgStruct.scalar_int('Marker_3'),
			ArgStruct.scalar_int('Marker_4'),
			ArgStruct.scalar_int('Restart_Marker')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Marker_2: int = None
			self.Marker_3: int = None
			self.Marker_4: int = None
			self.Restart_Marker: int = None

	def get(self) -> DelaysStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:ARB:MARKer:DELays \n
		Snippet: value: DelaysStruct = driver.source.afRf.generator.arb.marker.delays.get() \n
		Defines delay times for the generation of trigger signals relative to the marker events. All delay times are specified as
		number of samples. \n
			:return: structure: for return value, see the help for DelaysStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:AFRF:GENerator<Instance>:ARB:MARKer:DELays?', self.__class__.DelaysStruct())
