from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def set(self, filter_left_frequency: float, filter_right_frequency: float, notch=repcap.Notch.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh<Num>:FREQuency \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.notch.frequency.set(filter_left_frequency = 1.0, filter_right_frequency = 1.0, notch = repcap.Notch.Default) \n
		Sets the frequency for the notch filters 1, 2 or 3 of the left SPDIF IN or right SPDIF IN connectors. \n
			:param filter_left_frequency: Range: 5 Hz to 21000 Hz, Unit: Hz
			:param filter_right_frequency: Range: 5 Hz to 21000 Hz, Unit: Hz
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('filter_left_frequency', filter_left_frequency, DataType.Float), ArgSingle('filter_right_frequency', filter_right_frequency, DataType.Float))
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh{notch_cmd_val}:FREQuency {param}'.rstrip())

	# noinspection PyTypeChecker
	class FrequencyStruct(StructBase):
		"""Response structure. Fields: \n
			- Filter_Left_Frequency: float: Range: 5 Hz to 21000 Hz, Unit: Hz
			- Filter_Right_Frequency: float: Range: 5 Hz to 21000 Hz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Filter_Left_Frequency'),
			ArgStruct.scalar_float('Filter_Right_Frequency')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Filter_Left_Frequency: float = None
			self.Filter_Right_Frequency: float = None

	def get(self, notch=repcap.Notch.Default) -> FrequencyStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh<Num>:FREQuency \n
		Snippet: value: FrequencyStruct = driver.configure.afRf.measurement.spdif.filterPy.notch.frequency.get(notch = repcap.Notch.Default) \n
		Sets the frequency for the notch filters 1, 2 or 3 of the left SPDIF IN or right SPDIF IN connectors. \n
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: structure: for return value, see the help for FrequencyStruct structure arguments."""
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh{notch_cmd_val}:FREQuency?', self.__class__.FrequencyStruct())
