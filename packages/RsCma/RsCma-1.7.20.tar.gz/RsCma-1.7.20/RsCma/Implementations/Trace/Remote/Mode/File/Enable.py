from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, benable: bool, instrument=repcap.Instrument.Default) -> None:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:ENABle \n
		Snippet: driver.trace.remote.mode.file.enable.set(benable = False, instrument = repcap.Instrument.Default) \n
		Enables or disables tracing of the remote control interface to a file. \n
			:param benable: 1 | 0 1: Tracing is enabled. 0: Tracing is disabled. Default value: 0
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
		"""
		param = Conversions.bool_to_str(benable)
		instrument_cmd_val = self._cmd_group.get_repcap_cmd_value(instrument, repcap.Instrument)
		self._core.io.write(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:ENABle {param}')

	def get(self, instrument=repcap.Instrument.Default) -> bool:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:ENABle \n
		Snippet: value: bool = driver.trace.remote.mode.file.enable.get(instrument = repcap.Instrument.Default) \n
		Enables or disables tracing of the remote control interface to a file. \n
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
			:return: benable: No help available"""
		instrument_cmd_val = self._cmd_group.get_repcap_cmd_value(instrument, repcap.Instrument)
		response = self._core.io.query_str(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
