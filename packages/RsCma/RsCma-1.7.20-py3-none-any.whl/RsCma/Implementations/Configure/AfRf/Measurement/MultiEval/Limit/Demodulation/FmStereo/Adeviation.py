from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adeviation:
	"""Adeviation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("adeviation", core, parent)

	def set(self, enable: bool, upper: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:ADEViation \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.adeviation.set(enable = False, upper = 1.0) \n
		Configures a limit for the audio deviation results, measured for FM stereo. \n
			:param enable: OFF | ON Enables or disables the limit check
			:param upper: Upper audio deviation limit Range: 0 Hz to 100 kHz, Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:ADEViation {param}'.rstrip())

	# noinspection PyTypeChecker
	class AdeviationStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper audio deviation limit Range: 0 Hz to 100 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get(self) -> AdeviationStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:ADEViation \n
		Snippet: value: AdeviationStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.adeviation.get() \n
		Configures a limit for the audio deviation results, measured for FM stereo. \n
			:return: structure: for return value, see the help for AdeviationStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:ADEViation?', self.__class__.AdeviationStruct())
