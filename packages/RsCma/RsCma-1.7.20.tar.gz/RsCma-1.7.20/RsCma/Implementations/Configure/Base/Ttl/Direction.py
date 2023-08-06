from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Direction:
	"""Direction commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("direction", core, parent)

	def set(self, direction: enums.DirectionIo, tTL=repcap.TTL.Default) -> None:
		"""SCPI: CONFigure:BASE:TTL<Index>:DIRection \n
		Snippet: driver.configure.base.ttl.direction.set(direction = enums.DirectionIo.IN, tTL = repcap.TTL.Default) \n
		Configures the direction of a TTL register of the CONTROL connector. The direction of register 1 is fixed and can only be
		queried. The direction of register 2 can be configured. \n
			:param direction: IN | OUT
			:param tTL: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Ttl')
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.DirectionIo)
		tTL_cmd_val = self._cmd_group.get_repcap_cmd_value(tTL, repcap.TTL)
		self._core.io.write(f'CONFigure:BASE:TTL{tTL_cmd_val}:DIRection {param}')

	# noinspection PyTypeChecker
	def get(self, tTL=repcap.TTL.Default) -> enums.DirectionIo:
		"""SCPI: CONFigure:BASE:TTL<Index>:DIRection \n
		Snippet: value: enums.DirectionIo = driver.configure.base.ttl.direction.get(tTL = repcap.TTL.Default) \n
		Configures the direction of a TTL register of the CONTROL connector. The direction of register 1 is fixed and can only be
		queried. The direction of register 2 can be configured. \n
			:param tTL: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Ttl')
			:return: direction: IN | OUT"""
		tTL_cmd_val = self._cmd_group.get_repcap_cmd_value(tTL, repcap.TTL)
		response = self._core.io.query_str(f'CONFigure:BASE:TTL{tTL_cmd_val}:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.DirectionIo)
