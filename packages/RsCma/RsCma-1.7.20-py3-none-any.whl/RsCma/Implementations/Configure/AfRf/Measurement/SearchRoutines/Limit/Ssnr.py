from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ssnr:
	"""Ssnr commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("ssnr", core, parent)

	def set(self, enable: bool, upper: float, lower: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:SSNR \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.ssnr.set(enable = False, upper = 1.0, lower = 1.0) \n
		Enables a limit check and sets limits for the determined SNR. \n
			:param enable: OFF | ON
			:param upper: Unit: dB
			:param lower: Unit: dB
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('upper', upper, DataType.Float), ArgSingle('lower', lower, DataType.Float))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:SSNR {param}'.rstrip())

	# noinspection PyTypeChecker
	class SsnrStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON
			- Upper: float: Unit: dB
			- Lower: float: Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper'),
			ArgStruct.scalar_float('Lower')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None
			self.Lower: float = None

	def get(self) -> SsnrStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:SSNR \n
		Snippet: value: SsnrStruct = driver.configure.afRf.measurement.searchRoutines.limit.ssnr.get() \n
		Enables a limit check and sets limits for the determined SNR. \n
			:return: structure: for return value, see the help for SsnrStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:SSNR?', self.__class__.SsnrStruct())
