from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, filter_left_enable: bool, filter_right_enable: bool, notch=repcap.Notch.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh<Num>:ENABle \n
		Snippet: driver.configure.afRf.measurement.spdif.filterPy.notch.enable.set(filter_left_enable = False, filter_right_enable = False, notch = repcap.Notch.Default) \n
		Enables the notch filters 1, 2 or 3 of the left SPDIF IN or right SPDIF IN connectors. \n
			:param filter_left_enable: OFF | ON
			:param filter_right_enable: OFF | ON
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('filter_left_enable', filter_left_enable, DataType.Boolean), ArgSingle('filter_right_enable', filter_right_enable, DataType.Boolean))
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh{notch_cmd_val}:ENABle {param}'.rstrip())

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Response structure. Fields: \n
			- Filter_Left_Enable: bool: OFF | ON
			- Filter_Right_Enable: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Filter_Left_Enable'),
			ArgStruct.scalar_bool('Filter_Right_Enable')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Filter_Left_Enable: bool = None
			self.Filter_Right_Enable: bool = None

	def get(self, notch=repcap.Notch.Default) -> EnableStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh<Num>:ENABle \n
		Snippet: value: EnableStruct = driver.configure.afRf.measurement.spdif.filterPy.notch.enable.get(notch = repcap.Notch.Default) \n
		Enables the notch filters 1, 2 or 3 of the left SPDIF IN or right SPDIF IN connectors. \n
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: structure: for return value, see the help for EnableStruct structure arguments."""
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:FILTer:NOTCh{notch_cmd_val}:ENABle?', self.__class__.EnableStruct())
