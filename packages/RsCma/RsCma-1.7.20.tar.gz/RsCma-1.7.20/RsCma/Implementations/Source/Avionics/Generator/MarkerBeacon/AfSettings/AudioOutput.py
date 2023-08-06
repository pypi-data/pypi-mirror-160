from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AudioOutput:
	"""AudioOutput commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("audioOutput", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:AOUT:ENABle \n
		Snippet: value: bool = driver.source.avionics.generator.markerBeacon.afSettings.audioOutput.get_enable() \n
		Enables or disables the AF output path. \n
			:return: af_enable: OFF | ON
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:AOUT:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, af_enable: bool) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:AOUT:ENABle \n
		Snippet: driver.source.avionics.generator.markerBeacon.afSettings.audioOutput.set_enable(af_enable = False) \n
		Enables or disables the AF output path. \n
			:param af_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(af_enable)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:AOUT:ENABle {param}')

	def get_level(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:AOUT:LEVel \n
		Snippet: value: float = driver.source.avionics.generator.markerBeacon.afSettings.audioOutput.get_level() \n
		Specifies the output level for the AF output path. \n
			:return: level: Range: 10E-6 V to 5 V, Unit: V
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:AOUT:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:AOUT:LEVel \n
		Snippet: driver.source.avionics.generator.markerBeacon.afSettings.audioOutput.set_level(level = 1.0) \n
		Specifies the output level for the AF output path. \n
			:param level: Range: 10E-6 V to 5 V, Unit: V
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:MBEacon:AFSettings:AOUT:LEVel {param}')
