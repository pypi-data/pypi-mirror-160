from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.RepeatedCapability import RepeatedCapability
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Battery:
	"""Battery commands group definition. 5 total commands, 1 Subgroups, 4 group commands
	Repeated Capability: Battery, default value after init: Battery.Ix1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("battery", core, parent)
		self._cmd_group.rep_cap = RepeatedCapability(self._cmd_group.group_name, 'repcap_battery_get', 'repcap_battery_set', repcap.Battery.Ix1)

	def repcap_battery_set(self, battery: repcap.Battery) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Battery.Default
		Default value after init: Battery.Ix1"""
		self._cmd_group.set_repcap_enum_value(battery)

	def repcap_battery_get(self) -> repcap.Battery:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._cmd_group.get_repcap_enum_value()

	@property
	def info(self):
		"""info commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_info'):
			from .Info import Info
			self._info = Info(self._core, self._cmd_group)
		return self._info

	def get_available(self) -> bool:
		"""SCPI: SENSe:BASE:BATTery:AVAilable \n
		Snippet: value: bool = driver.sense.base.battery.get_available() \n
		Queries if at least one battery is inserted. \n
			:return: batt_available: OFF | ON OFF: No battery inserted ON: One or two batteries inserted
		"""
		response = self._core.io.query_str('SENSe:BASE:BATTery:AVAilable?')
		return Conversions.str_to_bool(response)

	def get_capacity(self) -> float:
		"""SCPI: SENSe:BASE:BATTery:CAPacity \n
		Snippet: value: float = driver.sense.base.battery.get_capacity() \n
		Queries the total capacity (sum of available batteries) . \n
			:return: batt_capacity: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SENSe:BASE:BATTery:CAPacity?')
		return Conversions.str_to_float(response)

	def get_ttd(self) -> int:
		"""SCPI: SENSe:BASE:BATTery:TTD \n
		Snippet: value: int = driver.sense.base.battery.get_ttd() \n
		Queries the estimated total remaining runtime for the sum of all available batteries. The value is calculated from the
		total capacity and the current discharge rate of the used battery. \n
			:return: ttd: Time until discharged Unit: s
		"""
		response = self._core.io.query_str('SENSe:BASE:BATTery:TTD?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_usage(self) -> List[enums.BatteryUsage]:
		"""SCPI: SENSe:BASE:BATTery:USAGe \n
		Snippet: value: List[enums.BatteryUsage] = driver.sense.base.battery.get_usage() \n
		Queries the state of both slots of the battery compartment. Two values are returned: <BattUsage>slot 1, <BattUsage>slot 2 \n
			:return: batt_usage: NAV | REMovable | USED NAV Slot empty REMovable Battery inserted but currently not used - can be removed USED Battery currently used - do not remove it
		"""
		response = self._core.io.query_str('SENSe:BASE:BATTery:USAGe?')
		return Conversions.str_to_list_enum(response, enums.BatteryUsage)

	def clone(self) -> 'Battery':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Battery(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
