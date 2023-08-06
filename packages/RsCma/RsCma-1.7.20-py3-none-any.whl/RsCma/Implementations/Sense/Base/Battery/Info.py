from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Info:
	"""Info commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("info", core, parent)

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Usage: enums.BatteryUsage: NAV | REMovable | USED NAV Slot empty REMovable Battery inserted but currently not used - can be removed USED Battery currently used - do not remove it
			- Capacity: float: Battery capacity Unit: %
			- Design_Cap: float: Nominal capacity stated by the battery manufacturer Unit: Wh
			- Full_Ch_Cap: float: Full-charge capacity of the battery Unit: Wh
			- Voltage: float: Battery voltage Unit: V
			- Temp: float: Battery temperature Unit: °C
			- Disch_Rate: float: Discharge rate Unit: W
			- Cycle_Count: int: Charge/discharge cycles
			- Dev_Name: str: Battery name as string
			- Serial_Nr: str: Battery serial number as string
			- Manufacturer_Name: str: Battery manufacturer as string
			- Manufacture_Date: str: Battery manufacturing date as string"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Usage', enums.BatteryUsage),
			ArgStruct.scalar_float('Capacity'),
			ArgStruct.scalar_float('Design_Cap'),
			ArgStruct.scalar_float('Full_Ch_Cap'),
			ArgStruct.scalar_float('Voltage'),
			ArgStruct.scalar_float('Temp'),
			ArgStruct.scalar_float('Disch_Rate'),
			ArgStruct.scalar_int('Cycle_Count'),
			ArgStruct.scalar_str('Dev_Name'),
			ArgStruct.scalar_str('Serial_Nr'),
			ArgStruct.scalar_str('Manufacturer_Name'),
			ArgStruct.scalar_str('Manufacture_Date')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Usage: enums.BatteryUsage = None
			self.Capacity: float = None
			self.Design_Cap: float = None
			self.Full_Ch_Cap: float = None
			self.Voltage: float = None
			self.Temp: float = None
			self.Disch_Rate: float = None
			self.Cycle_Count: int = None
			self.Dev_Name: str = None
			self.Serial_Nr: str = None
			self.Manufacturer_Name: str = None
			self.Manufacture_Date: str = None

	def get(self, battery=repcap.Battery.Default) -> GetStruct:
		"""SCPI: SENSe:BASE:BATTery<BattIdx>:INFO \n
		Snippet: value: GetStruct = driver.sense.base.battery.info.get(battery = repcap.Battery.Default) \n
		Queries information for a battery slot. \n
			:param battery: optional repeated capability selector. Default value: Ix1 (settable in the interface 'Battery')
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		battery_cmd_val = self._cmd_group.get_repcap_cmd_value(battery, repcap.Battery)
		return self._core.io.query_struct(f'SENSe:BASE:BATTery{battery_cmd_val}:INFO?', self.__class__.GetStruct())
