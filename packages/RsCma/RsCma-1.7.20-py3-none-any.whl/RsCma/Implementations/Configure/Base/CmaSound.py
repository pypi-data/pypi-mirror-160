from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CmaSound:
	"""CmaSound commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cmaSound", core, parent)

	def get_volume(self) -> int or bool:
		"""SCPI: CONFigure:BASE:CMASound:VOLume \n
		Snippet: value: int or bool = driver.configure.base.cmaSound.get_volume() \n
		Configures the volume of the monitored CMA sound. \n
			:return: cma_sound: (integer or boolean) OFF Switches off the CMA sound without changing the volume setting ON Switches on the CMA sound without changing the volume setting number A number greater than zero sets the volume and switches on the CMA sound. Zero sets the volume and switches off the CMA sound. Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('CONFigure:BASE:CMASound:VOLume?')
		return Conversions.str_to_int_or_bool(response)

	def set_volume(self, cma_sound: int or bool) -> None:
		"""SCPI: CONFigure:BASE:CMASound:VOLume \n
		Snippet: driver.configure.base.cmaSound.set_volume(cma_sound = 1) \n
		Configures the volume of the monitored CMA sound. \n
			:param cma_sound: (integer or boolean) OFF Switches off the CMA sound without changing the volume setting ON Switches on the CMA sound without changing the volume setting number A number greater than zero sets the volume and switches on the CMA sound. Zero sets the volume and switches off the CMA sound. Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_or_bool_value_to_str(cma_sound)
		self._core.io.write(f'CONFigure:BASE:CMASound:VOLume {param}')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.SoundSource:
		"""SCPI: CONFigure:BASE:CMASound:SOURce \n
		Snippet: value: enums.SoundSource = driver.configure.base.cmaSound.get_source() \n
		Selects the audio source to be connected to the loudspeaker / headphones. \n
			:return: sound_source: GENone | GENThree | AFONe | SPDif | DEModulator | LAN GENone Generator 1 + generator 2 GENThree Generator 3 + generator 4 AFONe AF1 IN + AF2 IN SPDif SPDIF IN L + R DEModulator Demodulator output LAN LAN connector (voice over IP)
		"""
		response = self._core.io.query_str('CONFigure:BASE:CMASound:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.SoundSource)

	def set_source(self, sound_source: enums.SoundSource) -> None:
		"""SCPI: CONFigure:BASE:CMASound:SOURce \n
		Snippet: driver.configure.base.cmaSound.set_source(sound_source = enums.SoundSource.AFONe) \n
		Selects the audio source to be connected to the loudspeaker / headphones. \n
			:param sound_source: GENone | GENThree | AFONe | SPDif | DEModulator | LAN GENone Generator 1 + generator 2 GENThree Generator 3 + generator 4 AFONe AF1 IN + AF2 IN SPDif SPDIF IN L + R DEModulator Demodulator output LAN LAN connector (voice over IP)
		"""
		param = Conversions.enum_scalar_to_str(sound_source, enums.SoundSource)
		self._core.io.write(f'CONFigure:BASE:CMASound:SOURce {param}')

	def get_squelch(self) -> bool:
		"""SCPI: CONFigure:BASE:CMASound:SQUelch \n
		Snippet: value: bool = driver.configure.base.cmaSound.get_squelch() \n
		Enables the squelch function if you use the demodulator output as source. Impacts the AF1 OUT and AF2 OUT connectors if
		you configure it to use the demodulator signal. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BASE:CMASound:SQUelch?')
		return Conversions.str_to_bool(response)

	def set_squelch(self, enable: bool) -> None:
		"""SCPI: CONFigure:BASE:CMASound:SQUelch \n
		Snippet: driver.configure.base.cmaSound.set_squelch(enable = False) \n
		Enables the squelch function if you use the demodulator output as source. Impacts the AF1 OUT and AF2 OUT connectors if
		you configure it to use the demodulator signal. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BASE:CMASound:SQUelch {param}')
