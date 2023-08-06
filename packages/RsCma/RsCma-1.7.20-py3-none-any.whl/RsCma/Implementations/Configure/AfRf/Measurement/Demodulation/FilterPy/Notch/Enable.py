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

	def set(self, notch_filter_enable: bool, notch=repcap.Notch.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:NOTCh<Num>:ENABle \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.notch.enable.set(notch_filter_enable = False, notch = repcap.Notch.Default) \n
		Enables the notch filters 1, 2 or 3 of the 'Demod' path. \n
			:param notch_filter_enable: OFF | ON
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
		"""
		param = Conversions.bool_to_str(notch_filter_enable)
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:NOTCh{notch_cmd_val}:ENABle {param}')

	def get(self, notch=repcap.Notch.Default) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:NOTCh<Num>:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.demodulation.filterPy.notch.enable.get(notch = repcap.Notch.Default) \n
		Enables the notch filters 1, 2 or 3 of the 'Demod' path. \n
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: notch_filter_enable: OFF | ON"""
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:NOTCh{notch_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
