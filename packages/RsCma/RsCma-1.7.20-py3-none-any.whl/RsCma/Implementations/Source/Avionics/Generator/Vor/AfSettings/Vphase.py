from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vphase:
	"""Vphase commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("vphase", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:ENABle \n
		Snippet: value: bool = driver.source.avionics.generator.vor.afSettings.vphase.get_enable() \n
		Enables or disables the VAR signal. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:ENABle \n
		Snippet: driver.source.avionics.generator.vor.afSettings.vphase.set_enable(enable = False) \n
		Enables or disables the VAR signal. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:ENABle {param}')

	def get_mod_depth(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:MDEPth \n
		Snippet: value: float = driver.source.avionics.generator.vor.afSettings.vphase.get_mod_depth() \n
		Sets the AM modulation depth for the VAR signal. The sum of the modulation depths for all enabled components must not
		exceed 100 %. \n
			:return: vor_mod_depth: Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:MDEPth?')
		return Conversions.str_to_float(response)

	def set_mod_depth(self, vor_mod_depth: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:MDEPth \n
		Snippet: driver.source.avionics.generator.vor.afSettings.vphase.set_mod_depth(vor_mod_depth = 1.0) \n
		Sets the AM modulation depth for the VAR signal. The sum of the modulation depths for all enabled components must not
		exceed 100 %. \n
			:param vor_mod_depth: Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_value_to_str(vor_mod_depth)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:MDEPth {param}')

	def get_bangle(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:BANGle \n
		Snippet: value: float = driver.source.avionics.generator.vor.afSettings.vphase.get_bangle() \n
		Sets the bearing angle from the beacon to the receiver, or vice versa, depending on the configured direction. \n
			:return: vor_phase: Range: 0 deg to 360 deg, Unit: deg
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:BANGle?')
		return Conversions.str_to_float(response)

	def set_bangle(self, vor_phase: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:BANGle \n
		Snippet: driver.source.avionics.generator.vor.afSettings.vphase.set_bangle(vor_phase = 1.0) \n
		Sets the bearing angle from the beacon to the receiver, or vice versa, depending on the configured direction. \n
			:param vor_phase: Range: 0 deg to 360 deg, Unit: deg
		"""
		param = Conversions.decimal_value_to_str(vor_phase)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:BANGle {param}')

	# noinspection PyTypeChecker
	def get_direction(self) -> enums.VphaseDirection:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:DIRection \n
		Snippet: value: enums.VphaseDirection = driver.source.avionics.generator.vor.afSettings.vphase.get_direction() \n
		Sets the bearing direction. \n
			:return: direction: TO | FROM TO The bearing angle indicates the clockwise angle between north and the line from the receiver to the beacon. FROM The bearing angle indicates the clockwise angle between north and the line from the beacon to the receiver.
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:DIRection?')
		return Conversions.str_to_scalar_enum(response, enums.VphaseDirection)

	def set_direction(self, direction: enums.VphaseDirection) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:DIRection \n
		Snippet: driver.source.avionics.generator.vor.afSettings.vphase.set_direction(direction = enums.VphaseDirection.FROM) \n
		Sets the bearing direction. \n
			:param direction: TO | FROM TO The bearing angle indicates the clockwise angle between north and the line from the receiver to the beacon. FROM The bearing angle indicates the clockwise angle between north and the line from the beacon to the receiver.
		"""
		param = Conversions.enum_scalar_to_str(direction, enums.VphaseDirection)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:VOR:AFSettings:VPHase:DIRection {param}')
