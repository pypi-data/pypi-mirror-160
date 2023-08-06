from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, filter_enable: bool, audioInput=repcap.AudioInput.Default, notch=repcap.Notch.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:NOTCh<Num>:ENABle \n
		Snippet: driver.configure.afRf.measurement.audioInput.filterPy.notch.enable.set(filter_enable = False, audioInput = repcap.AudioInput.Default, notch = repcap.Notch.Default) \n
		Enables the notch filters 1, 2 or 3 of the AF1 IN or AF2 IN connectors. \n
			:param filter_enable: OFF | ON
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
		"""
		param = Conversions.bool_to_str(filter_enable)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:NOTCh{notch_cmd_val}:ENABle {param}')

	def get(self, audioInput=repcap.AudioInput.Default, notch=repcap.Notch.Default) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:NOTCh<Num>:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.audioInput.filterPy.notch.enable.get(audioInput = repcap.AudioInput.Default, notch = repcap.Notch.Default) \n
		Enables the notch filters 1, 2 or 3 of the AF1 IN or AF2 IN connectors. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: filter_enable: OFF | ON"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:NOTCh{notch_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
