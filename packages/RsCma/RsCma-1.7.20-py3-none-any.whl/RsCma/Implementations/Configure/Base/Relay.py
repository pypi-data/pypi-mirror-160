from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Relay:
	"""Relay commands group definition. 1 total commands, 0 Subgroups, 1 group commands
	Repeated Capability: Relay, default value after init: Relay.Ix1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("relay", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_relay_get', 'repcap_relay_set', repcap.Relay.Ix1)

	def repcap_relay_set(self, relay: repcap.Relay) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Relay.Default
		Default value after init: Relay.Ix1"""
		self._cmd_group.set_repcap_enum_value(relay)

	def repcap_relay_get(self) -> repcap.Relay:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	def set(self, activity: enums.Activity, relay=repcap.Relay.Default) -> None:
		"""SCPI: CONFigure:BASE:RELay<Index> \n
		Snippet: driver.configure.base.relay.set(activity = enums.Activity.ACTive, relay = repcap.Relay.Default) \n
		Activates or deactivates relay 1 or 2 of the CONTROL connector. \n
			:param activity: INACtive | ACTive
			:param relay: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Relay')
		"""
		param = Conversions.enum_scalar_to_str(activity, enums.Activity)
		relay_cmd_val = self._cmd_group.get_repcap_cmd_value(relay, repcap.Relay)
		self._core.io.write(f'CONFigure:BASE:RELay{relay_cmd_val} {param}')

	# noinspection PyTypeChecker
	def get(self, relay=repcap.Relay.Default) -> enums.Activity:
		"""SCPI: CONFigure:BASE:RELay<Index> \n
		Snippet: value: enums.Activity = driver.configure.base.relay.get(relay = repcap.Relay.Default) \n
		Activates or deactivates relay 1 or 2 of the CONTROL connector. \n
			:param relay: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Relay')
			:return: activity: INACtive | ACTive"""
		relay_cmd_val = self._cmd_group.get_repcap_cmd_value(relay, repcap.Relay)
		response = self._core.io.query_str(f'CONFigure:BASE:RELay{relay_cmd_val}?')
		return Conversions.str_to_scalar_enum(response, enums.Activity)

	def clone(self) -> 'Relay':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Relay(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
