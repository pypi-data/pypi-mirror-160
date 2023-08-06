from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Name:
	"""Name commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("name", core, parent)

	def set(self, bs_file_path: str, instrument=repcap.Instrument.Default) -> None:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:NAME \n
		Snippet: driver.trace.remote.mode.file.name.set(bs_file_path = '1', instrument = repcap.Instrument.Default) \n
		Specifies path and name of the target file for tracing of the remote control interface. If you specify a new target file
		while tracing, the old target file is closed, the new file is created and tracing is continued with the new file. \n
			:param bs_file_path: String parameter specifying path and name of the file Default value: 'D:/Rohde-Schwarz/CMA/Log/version/RemoteTrace-Inst0.xml'
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
		"""
		param = Conversions.value_to_quoted_str(bs_file_path)
		instrument_cmd_val = self._cmd_group.get_repcap_cmd_value(instrument, repcap.Instrument)
		self._core.io.write(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:NAME {param}')

	def get(self, instrument=repcap.Instrument.Default) -> str:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:NAME \n
		Snippet: value: str = driver.trace.remote.mode.file.name.get(instrument = repcap.Instrument.Default) \n
		Specifies path and name of the target file for tracing of the remote control interface. If you specify a new target file
		while tracing, the old target file is closed, the new file is created and tracing is continued with the new file. \n
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
			:return: bs_file_path: No help available"""
		instrument_cmd_val = self._cmd_group.get_repcap_cmd_value(instrument, repcap.Instrument)
		response = self._core.io.query_str(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:NAME?')
		return trim_str_response(response)
