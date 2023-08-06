from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.Types import DataType
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct
from .........Internal.ArgSingleList import ArgSingleList
from .........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rms:
	"""Rms commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rms", core, parent)

	def set(self, enable: bool, upper: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:RMS \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.pdeviation.rms.set(enable = False, upper = 1.0) \n
		Configures a limit for the 'RMS' phase deviation results, measured for PM. \n
			:param enable: OFF | ON Enables or disables the limit check
			:param upper: Upper phase deviation limit Range: 0 rad to 10 rad, Unit: rad
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('upper', upper, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:RMS {param}'.rstrip())

	# noinspection PyTypeChecker
	class RmsStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper phase deviation limit Range: 0 rad to 10 rad, Unit: rad"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get(self) -> RmsStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:RMS \n
		Snippet: value: RmsStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.pdeviation.rms.get() \n
		Configures a limit for the 'RMS' phase deviation results, measured for PM. \n
			:return: structure: for return value, see the help for RmsStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:PDEViation:RMS?', self.__class__.RmsStruct())
