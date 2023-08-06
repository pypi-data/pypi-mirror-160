from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Update:
	"""Update commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("update", core, parent)

	def set(self, tTL=repcap.TTL.Default) -> None:
		"""SCPI: CONFigure:BASE:TTL<Index>:UPDate \n
		Snippet: driver.configure.base.ttl.update.set(tTL = repcap.TTL.Default) \n
		If TTL2 is used in input direction, this command triggers the evaluation of the input signal and a refresh of the
		resulting bit values. \n
			:param tTL: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Ttl')
		"""
		tTL_cmd_val = self._cmd_group.get_repcap_cmd_value(tTL, repcap.TTL)
		self._core.io.write(f'CONFigure:BASE:TTL{tTL_cmd_val}:UPDate')

	def set_with_opc(self, tTL=repcap.TTL.Default, opc_timeout_ms: int = -1) -> None:
		tTL_cmd_val = self._cmd_group.get_repcap_cmd_value(tTL, repcap.TTL)
		"""SCPI: CONFigure:BASE:TTL<Index>:UPDate \n
		Snippet: driver.configure.base.ttl.update.set_with_opc(tTL = repcap.TTL.Default) \n
		If TTL2 is used in input direction, this command triggers the evaluation of the input signal and a refresh of the
		resulting bit values. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param tTL: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Ttl')
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:BASE:TTL{tTL_cmd_val}:UPDate', opc_timeout_ms)
