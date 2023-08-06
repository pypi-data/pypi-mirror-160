from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StartMode:
	"""StartMode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("startMode", core, parent)

	def set(self, estart_mode: enums.EstartMode, instrument=repcap.Instrument.Default) -> None:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:STARtmode \n
		Snippet: driver.trace.remote.mode.file.startMode.set(estart_mode = enums.EstartMode.AUTO, instrument = repcap.Instrument.Default) \n
		Specifies whether tracing is started automatically or manually. \n
			:param estart_mode: AUTO | EXPLicit AUTO Start tracing automatically when the instrument is started. EXPLicit Start tracing via the command method RsCma.Trace.Remote.Mode.File.Enable.set. Default value: EXPLicit
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
		"""
		param = Conversions.enum_scalar_to_str(estart_mode, enums.EstartMode)
		instrument_cmd_val = self._cmd_group.get_repcap_cmd_value(instrument, repcap.Instrument)
		self._core.io.write(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:STARtmode {param}')

	# noinspection PyTypeChecker
	def get(self, instrument=repcap.Instrument.Default) -> enums.EstartMode:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:STARtmode \n
		Snippet: value: enums.EstartMode = driver.trace.remote.mode.file.startMode.get(instrument = repcap.Instrument.Default) \n
		Specifies whether tracing is started automatically or manually. \n
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
			:return: estart_mode: AUTO | EXPLicit AUTO Start tracing automatically when the instrument is started. EXPLicit Start tracing via the command method RsCma.Trace.Remote.Mode.File.Enable.set. Default value: EXPLicit"""
		instrument_cmd_val = self._cmd_group.get_repcap_cmd_value(instrument, repcap.Instrument)
		response = self._core.io.query_str(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:STARtmode?')
		return Conversions.str_to_scalar_enum(response, enums.EstartMode)
