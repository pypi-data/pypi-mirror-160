from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def set(self, filter_frequency: float, audioInput=repcap.AudioInput.Default, notch=repcap.Notch.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:NOTCh<Num>:FREQuency \n
		Snippet: driver.configure.afRf.measurement.audioInput.filterPy.notch.frequency.set(filter_frequency = 1.0, audioInput = repcap.AudioInput.Default, notch = repcap.Notch.Default) \n
		Sets the frequency for the notch filters 1, 2 or 3 of the AF1 IN or AF2 IN connectors. \n
			:param filter_frequency: Range: 5 Hz to 21000 Hz, Unit: Hz
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
		"""
		param = Conversions.decimal_value_to_str(filter_frequency)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:NOTCh{notch_cmd_val}:FREQuency {param}')

	def get(self, audioInput=repcap.AudioInput.Default, notch=repcap.Notch.Default) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:NOTCh<Num>:FREQuency \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.filterPy.notch.frequency.get(audioInput = repcap.AudioInput.Default, notch = repcap.Notch.Default) \n
		Sets the frequency for the notch filters 1, 2 or 3 of the AF1 IN or AF2 IN connectors. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: filter_frequency: Range: 5 Hz to 21000 Hz, Unit: Hz"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:NOTCh{notch_cmd_val}:FREQuency?')
		return Conversions.str_to_float(response)
