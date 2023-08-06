from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rms:
	"""Rms commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rms", core, parent)

	def set(self, enable: bool, limit: float) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:FFERor:RMS \n
		Snippet: driver.configure.vse.measurement.limit.dpmr.ffError.rms.set(enable = False, limit = 1.0) \n
		Configures an upper limit for the measured 'RMS' value of the FSK frequency error for the digital standard 'DPMR'. \n
			:param enable: OFF | ON
			:param limit: Upper FSK frequency error limit for 'RMS' value Range: 0 % to 100 %, Unit: %
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('limit', limit, DataType.Float))
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:FFERor:RMS {param}'.rstrip())

	# noinspection PyTypeChecker
	class RmsStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON
			- Limit: float: Upper FSK frequency error limit for 'RMS' value Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get(self) -> RmsStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:FFERor:RMS \n
		Snippet: value: RmsStruct = driver.configure.vse.measurement.limit.dpmr.ffError.rms.get() \n
		Configures an upper limit for the measured 'RMS' value of the FSK frequency error for the digital standard 'DPMR'. \n
			:return: structure: for return value, see the help for RmsStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:VSE:MEASurement<Instance>:LIMit:DPMR:FFERor:RMS?', self.__class__.RmsStruct())
