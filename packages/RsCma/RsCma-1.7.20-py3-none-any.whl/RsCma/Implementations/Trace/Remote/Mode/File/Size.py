from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Size:
	"""Size commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("size", core, parent)

	def set(self, ifile_size: int, instrument=repcap.Instrument.Default) -> None:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:SIZE \n
		Snippet: driver.trace.remote.mode.file.size.set(ifile_size = 1, instrument = repcap.Instrument.Default) \n
		Specifies the maximum trace file size in bytes. \n
			:param ifile_size: Recommended minimum value: 40000 bytes Maximum value: 1000000000 bytes (1 GB) Default value: 1000000000 bytes (1 GB)
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
		"""
		param = Conversions.decimal_value_to_str(ifile_size)
		instrument_cmd_val = self._cmd_group.get_repcap_cmd_value(instrument, repcap.Instrument)
		self._core.io.write(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:SIZE {param}')

	def get(self, instrument=repcap.Instrument.Default) -> int:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:SIZE \n
		Snippet: value: int = driver.trace.remote.mode.file.size.get(instrument = repcap.Instrument.Default) \n
		Specifies the maximum trace file size in bytes. \n
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
			:return: ifile_size: No help available"""
		instrument_cmd_val = self._cmd_group.get_repcap_cmd_value(instrument, repcap.Instrument)
		response = self._core.io.query_str(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:SIZE?')
		return Conversions.str_to_int(response)
