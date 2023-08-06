from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sinad:
	"""Sinad commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sinad", core, parent)

	def set(self, enable: bool, lower: float, upper: float = None, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN<Nr>:SINad \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.audioInput.sinad.set(enable = False, lower = 1.0, upper = 1.0, audioInput = repcap.AudioInput.Default) \n
		Configures limits for the SINAD results, measured via an AF input path. \n
			:param enable: OFF | ON Enables or disables the limit check
			:param lower: Lower SINAD limit Range: 0 dB to 140 dB, Unit: dB
			:param upper: Upper SINAD limit Range: 0 dB to 140 dB, Unit: dB
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('lower', lower, DataType.Float), ArgSingle('upper', upper, DataType.Float, None, is_optional=True))
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN{audioInput_cmd_val}:SINad {param}'.rstrip())

	# noinspection PyTypeChecker
	class SinadStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower SINAD limit Range: 0 dB to 140 dB, Unit: dB
			- Upper: float: Upper SINAD limit Range: 0 dB to 140 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get(self, audioInput=repcap.AudioInput.Default) -> SinadStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN<Nr>:SINad \n
		Snippet: value: SinadStruct = driver.configure.afRf.measurement.multiEval.limit.audioInput.sinad.get(audioInput = repcap.AudioInput.Default) \n
		Configures limits for the SINAD results, measured via an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: structure: for return value, see the help for SinadStruct structure arguments."""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:AIN{audioInput_cmd_val}:SINad?', self.__class__.SinadStruct())
