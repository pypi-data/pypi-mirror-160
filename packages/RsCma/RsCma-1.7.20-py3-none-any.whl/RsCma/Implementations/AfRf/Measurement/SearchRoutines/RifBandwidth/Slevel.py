from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slevel:
	"""Slevel commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("slevel", core, parent)

	# noinspection PyTypeChecker
	class ResultData(StructBase):
		"""Response structure. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Lower_Signal_Level: float: Signal quality level at the lower frequency Unit: dBm
			- Higher_Signal_Level: float: Signal quality level at the higher frequency Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_float('Lower_Signal_Level'),
			ArgStruct.scalar_float('Higher_Signal_Level')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Lower_Signal_Level: float = None
			self.Higher_Signal_Level: float = None

	def fetch(self) -> ResultData:
		"""SCPI: FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:SLEVel \n
		Snippet: value: ResultData = driver.afRf.measurement.searchRoutines.rifBandwidth.slevel.fetch() \n
		Query the signal quality level at the lower and higher frequency. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'FETCh:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:SLEVel?', self.__class__.ResultData())

	def read(self) -> ResultData:
		"""SCPI: READ:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:SLEVel \n
		Snippet: value: ResultData = driver.afRf.measurement.searchRoutines.rifBandwidth.slevel.read() \n
		Query the signal quality level at the lower and higher frequency. \n
			:return: structure: for return value, see the help for ResultData structure arguments."""
		return self._core.io.query_struct(f'READ:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:SLEVel?', self.__class__.ResultData())
