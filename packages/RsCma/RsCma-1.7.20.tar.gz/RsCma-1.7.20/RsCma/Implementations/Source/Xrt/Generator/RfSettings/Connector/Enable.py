from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Enable:
	"""Enable commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("enable", core, parent)

	def set(self, enable: bool, connector=repcap.Connector.Default) -> None:
		"""SCPI: SOURce:XRT:GENerator<Instance>:RFSettings:CONNector<nr>:ENABle \n
		Snippet: driver.source.xrt.generator.rfSettings.connector.enable.set(enable = False, connector = repcap.Connector.Default) \n
		Activates the required output connectors from 'RF 1' to 'RF 8'. \n
			:param enable: OFF | ON
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
		"""
		param = Conversions.bool_to_str(enable)
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		self._core.io.write(f'SOURce:XRT:GENerator<Instance>:RFSettings:CONNector{connector_cmd_val}:ENABle {param}')

	def get(self, connector=repcap.Connector.Default) -> bool:
		"""SCPI: SOURce:XRT:GENerator<Instance>:RFSettings:CONNector<nr>:ENABle \n
		Snippet: value: bool = driver.source.xrt.generator.rfSettings.connector.enable.get(connector = repcap.Connector.Default) \n
		Activates the required output connectors from 'RF 1' to 'RF 8'. \n
			:param connector: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Connector')
			:return: enable: OFF | ON"""
		connector_cmd_val = self._cmd_group.get_repcap_cmd_value(connector, repcap.Connector)
		response = self._core.io.query_str(f'SOURce:XRT:GENerator<Instance>:RFSettings:CONNector{connector_cmd_val}:ENABle?')
		return Conversions.str_to_bool(response)
