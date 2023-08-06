from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.ArgSingleSuppressed import ArgSingleSuppressed
from .....Internal.Types import DataType
from .....Internal.Utilities import trim_str_response
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reliability:
	"""Reliability commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("reliability", core, parent)

	def get(self, details: str = None) -> str:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RELiability \n
		Snippet: value: str = driver.source.afRf.generator.reliability.get(details = '1') \n
		Queries whether the generator has detected an error or not. If you have problems to generate a signal, use this command
		for troubleshooting. The returned parameters comprise a reliability indicator value and optionally, an error reason. \n
		Use RsCma.reliability.last_value to read the updated reliability indicator. \n
			:param details: To return an error reason in addition to the reliability indicator value, append 'Details' to the query: SOUR:AFRF:GEN:REL? 'DETails'
			:return: reliability_msg: String indicating the error reason If there is no error (reliability value = 0) , the string is empty. The parameter is only returned if parameter Details = 'DETails'."""
		param = ArgSingleList().compose_cmd_string(ArgSingle('details', details, DataType.String, None, is_optional=True))
		suppressed = ArgSingleSuppressed(0, DataType.Integer, False, 1, 'Reliability')
		response = self._core.io.query_str_suppressed(f'SOURce:AFRF:GENerator<Instance>:RELiability? {param}'.rstrip(), suppressed)
		return trim_str_response(response)

	# noinspection PyTypeChecker
	class AllStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Reliability: int: See 'Reliability indicator values'
			- Reliability_Msg: str: String indicating the error reason If there is no error (reliability value = 0) , the string is empty.
			- Reliability_Add_Info: str: String providing additional information for an error If there is no error (reliability value = 0) , the string is empty."""
		__meta_args_list = [
			ArgStruct.scalar_int('Reliability', 'Reliability'),
			ArgStruct.scalar_str('Reliability_Msg'),
			ArgStruct.scalar_str('Reliability_Add_Info')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Reliability: int = None
			self.Reliability_Msg: str = None
			self.Reliability_Add_Info: str = None

	def get_all(self) -> AllStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:RELiability:ALL \n
		Snippet: value: AllStruct = driver.source.afRf.generator.reliability.get_all() \n
		Queries whether the generator has detected an error or not. If you have problems to generate a signal, use this command
		for troubleshooting. The returned parameters comprise a reliability indicator value, an error reason and an additional
		information string. \n
			:return: structure: for return value, see the help for AllStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:AFRF:GENerator<Instance>:RELiability:ALL?', self.__class__.AllStruct())
