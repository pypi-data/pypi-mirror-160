from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Peak:
	"""Peak commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("peak", core, parent)

	def set(self, enable: bool, limit: float) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:PTFive:FFERor:PEAK \n
		Snippet: driver.configure.vse.measurement.limit.ptFive.ffError.peak.set(enable = False, limit = 1.0) \n
		Configures an upper limit for the measured peak value of the frequency deviation error. \n
			:param enable: OFF | ON
			:param limit: 0.00 % to 100.00 % Unit: %
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('limit', limit, DataType.Float))
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:LIMit:PTFive:FFERor:PEAK {param}'.rstrip())

	# noinspection PyTypeChecker
	class PeakStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON
			- Limit: float: 0.00 % to 100.00 % Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get(self) -> PeakStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:PTFive:FFERor:PEAK \n
		Snippet: value: PeakStruct = driver.configure.vse.measurement.limit.ptFive.ffError.peak.get() \n
		Configures an upper limit for the measured peak value of the frequency deviation error. \n
			:return: structure: for return value, see the help for PeakStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:VSE:MEASurement<Instance>:LIMit:PTFive:FFERor:PEAK?', self.__class__.PeakStruct())
