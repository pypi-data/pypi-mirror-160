from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Capture:
	"""Capture commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("capture", core, parent)

	def set(self, capt_pre_trig: int, capt_post_trig: int = None, standard: enums.Standard = None) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:CAPTure \n
		Snippet: driver.configure.vse.measurement.iqRecorder.capture.set(capt_pre_trig = 1, capt_post_trig = 1, standard = enums.Standard.CUSTom) \n
		Sets or queries the number of samples to be received before IQ recording is started ('Pre Trigger') and after which IQ
		recording is stopped ('Post Trigger') . \n
			:param capt_pre_trig: Range: 1 Samples to 4194303
			:param capt_post_trig: Range: 1 Samples to 4194303
			:param standard: DMR | DPMR | NXDN | P25 | TETRa | LTE | SPECtrum | CUSTom DMR | DPMR | NXDN | P25 | TETRa | LTE Allows query of the number of samples. CUSTom Allows set and query of the number of samples.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('capt_pre_trig', capt_pre_trig, DataType.Integer), ArgSingle('capt_post_trig', capt_post_trig, DataType.Integer, None, is_optional=True), ArgSingle('standard', standard, DataType.Enum, enums.Standard, is_optional=True))
		self._core.io.write(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:CAPTure {param}'.rstrip())

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Capt_Pre_Trig: int: Range: 1 Samples to 4194303
			- Capt_Post_Trig: int: Range: 1 Samples to 4194303"""
		__meta_args_list = [
			ArgStruct.scalar_int('Capt_Pre_Trig'),
			ArgStruct.scalar_int('Capt_Post_Trig')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Capt_Pre_Trig: int = None
			self.Capt_Post_Trig: int = None

	def get(self) -> GetStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:IQRecorder:CAPTure \n
		Snippet: value: GetStruct = driver.configure.vse.measurement.iqRecorder.capture.get() \n
		Sets or queries the number of samples to be received before IQ recording is started ('Pre Trigger') and after which IQ
		recording is stopped ('Post Trigger') . \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:VSE:MEASurement<Instance>:IQRecorder:CAPTure?', self.__class__.GetStruct())
