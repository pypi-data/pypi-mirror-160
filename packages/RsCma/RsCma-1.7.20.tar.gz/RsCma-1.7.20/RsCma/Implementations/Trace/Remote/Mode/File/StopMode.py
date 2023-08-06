from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StopMode:
	"""StopMode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("stopMode", core, parent)

	def set(self, estop_mode: enums.EstopMode, instrument=repcap.Instrument.Default) -> None:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:STOPmode \n
		Snippet: driver.trace.remote.mode.file.stopMode.set(estop_mode = enums.EstopMode.AUTO, instrument = repcap.Instrument.Default) \n
		Specifies how / when tracing is stopped and the trace file is closed. \n
			:param estop_mode: AUTO | EXPLicit | ERRor | BUFFerfull AUTO Stop tracing automatically when the instrument is shut down. EXPLicit Stop tracing via method RsCma.Trace.Remote.Mode.File.Enable.set. ERRor Stop tracing when a SCPI error occurs. BUFFerfull Stop tracing when the maximum file size is reached. Default value: EXPLicit
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
		"""
		param = Conversions.enum_scalar_to_str(estop_mode, enums.EstopMode)
		instrument_cmd_val = self._cmd_group.get_repcap_cmd_value(instrument, repcap.Instrument)
		self._core.io.write(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:STOPmode {param}')

	# noinspection PyTypeChecker
	def get(self, instrument=repcap.Instrument.Default) -> enums.EstopMode:
		"""SCPI: TRACe:REMote:MODE:FILE<instrument>:STOPmode \n
		Snippet: value: enums.EstopMode = driver.trace.remote.mode.file.stopMode.get(instrument = repcap.Instrument.Default) \n
		Specifies how / when tracing is stopped and the trace file is closed. \n
			:param instrument: optional repeated capability selector. Default value: Nr1 (settable in the interface 'File')
			:return: estop_mode: AUTO | EXPLicit | ERRor | BUFFerfull AUTO Stop tracing automatically when the instrument is shut down. EXPLicit Stop tracing via method RsCma.Trace.Remote.Mode.File.Enable.set. ERRor Stop tracing when a SCPI error occurs. BUFFerfull Stop tracing when the maximum file size is reached. Default value: EXPLicit"""
		instrument_cmd_val = self._cmd_group.get_repcap_cmd_value(instrument, repcap.Instrument)
		response = self._core.io.query_str(f'TRACe:REMote:MODE:FILE{instrument_cmd_val}:STOPmode?')
		return Conversions.str_to_scalar_enum(response, enums.EstopMode)
