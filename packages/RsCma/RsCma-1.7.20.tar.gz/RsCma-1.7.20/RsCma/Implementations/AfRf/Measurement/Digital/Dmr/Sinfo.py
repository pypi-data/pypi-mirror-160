from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sinfo:
	"""Sinfo commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sinfo", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Color_Code: int: No parameter help available
			- Source_Address: int: No parameter help available
			- Target_Address: int: No parameter help available
			- Pi: int: No parameter help available
			- Pflag: int: No parameter help available
			- Flco: int: No parameter help available
			- Fid: int: No parameter help available
			- Data_Type: int: No parameter help available
			- Broadcast: int: No parameter help available
			- Privacy: int: No parameter help available
			- Pl: int: No parameter help available
			- Emergency: int: No parameter help available
			- Ovcm: int: Range: 0 to 15"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_int('Color_Code'),
			ArgStruct.scalar_int('Source_Address'),
			ArgStruct.scalar_int('Target_Address'),
			ArgStruct.scalar_int('Pi'),
			ArgStruct.scalar_int('Pflag'),
			ArgStruct.scalar_int('Flco'),
			ArgStruct.scalar_int('Fid'),
			ArgStruct.scalar_int('Data_Type'),
			ArgStruct.scalar_int('Broadcast'),
			ArgStruct.scalar_int('Privacy'),
			ArgStruct.scalar_int('Pl'),
			ArgStruct.scalar_int('Emergency'),
			ArgStruct.scalar_int('Ovcm')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Color_Code: int = None
			self.Source_Address: int = None
			self.Target_Address: int = None
			self.Pi: int = None
			self.Pflag: int = None
			self.Flco: int = None
			self.Fid: int = None
			self.Data_Type: int = None
			self.Broadcast: int = None
			self.Privacy: int = None
			self.Pl: int = None
			self.Emergency: int = None
			self.Ovcm: int = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:DIGital:DMR:SINFo \n
		Snippet: value: ResultData = driver.afRf.measurement.digital.dmr.sinfo.fetch() \n
		Fetches the signal information for the DMR standard. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:DIGital:DMR:SINFo?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:DIGital:DMR:SINFo \n
		Snippet: value: ResultData = driver.afRf.measurement.digital.dmr.sinfo.read() \n
		Fetches the signal information for the DMR standard. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:DIGital:DMR:SINFo?', self.__class__.ResultData())
