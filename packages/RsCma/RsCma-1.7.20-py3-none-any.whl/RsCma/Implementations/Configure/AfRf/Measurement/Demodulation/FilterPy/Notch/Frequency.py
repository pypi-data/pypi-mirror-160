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

	def set(self, notch_filter_frequency: float, notch=repcap.Notch.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:NOTCh<Num>:FREQuency \n
		Snippet: driver.configure.afRf.measurement.demodulation.filterPy.notch.frequency.set(notch_filter_frequency = 1.0, notch = repcap.Notch.Default) \n
		Sets the frequency for the notch filters 1, 2 or 3 of the 'Demod' path. \n
			:param notch_filter_frequency: Range: 5 Hz to 21000 Hz, Unit: Hz
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
		"""
		param = Conversions.decimal_value_to_str(notch_filter_frequency)
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:NOTCh{notch_cmd_val}:FREQuency {param}')

	def get(self, notch=repcap.Notch.Default) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:NOTCh<Num>:FREQuency \n
		Snippet: value: float = driver.configure.afRf.measurement.demodulation.filterPy.notch.frequency.get(notch = repcap.Notch.Default) \n
		Sets the frequency for the notch filters 1, 2 or 3 of the 'Demod' path. \n
			:param notch: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Notch')
			:return: notch_filter_frequency: Range: 5 Hz to 21000 Hz, Unit: Hz"""
		notch_cmd_val = self._cmd_group.get_repcap_cmd_value(notch, repcap.Notch)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:FILTer:NOTCh{notch_cmd_val}:FREQuency?')
		return Conversions.str_to_float(response)
