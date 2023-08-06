from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.RepeatedCapability import RepeatedCapability
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 35 total commands, 5 Subgroups, 0 group commands
	Repeated Capability: Channel, default value after init: Channel.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("demodulation", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_channel_get', 'repcap_channel_set', repcap.Channel.Nr1)

	def repcap_channel_set(self, channel: repcap.Channel) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Channel.Default
		Default value after init: Channel.Nr1"""
		self._cmd_group.set_repcap_enum_value(channel)

	def repcap_channel_get(self) -> repcap.Channel:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def marker(self):
		"""marker commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import Marker
			self._marker = Marker(self._core, self._cmd_group)
		return self._marker

	@property
	def pdeviation(self):
		"""pdeviation commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_pdeviation'):
			from .Pdeviation import Pdeviation
			self._pdeviation = Pdeviation(self._core, self._cmd_group)
		return self._pdeviation

	@property
	def modDepth(self):
		"""modDepth commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_modDepth'):
			from .ModDepth import ModDepth
			self._modDepth = ModDepth(self._core, self._cmd_group)
		return self._modDepth

	@property
	def usbPower(self):
		"""usbPower commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_usbPower'):
			from .UsbPower import UsbPower
			self._usbPower = UsbPower(self._core, self._cmd_group)
		return self._usbPower

	@property
	def lsbPower(self):
		"""lsbPower commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_lsbPower'):
			from .LsbPower import LsbPower
			self._lsbPower = LsbPower(self._core, self._cmd_group)
		return self._lsbPower

	def clone(self) -> 'Demodulation':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Demodulation(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
