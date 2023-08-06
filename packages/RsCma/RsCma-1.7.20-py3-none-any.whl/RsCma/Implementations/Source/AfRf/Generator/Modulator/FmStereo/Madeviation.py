from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Madeviation:
	"""Madeviation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("madeviation", core, parent)

	def set(self, max_audio_deviation: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:MADeviation \n
		Snippet: driver.source.afRf.generator.modulator.fmStereo.madeviation.set(max_audio_deviation = 1.0) \n
		Specifies the maximum frequency deviation for the audio signal component of a generated FM stereo multiplex signal. The
		allowed range depends on the frequency deviation of the other signal components. The total deviation of the multiplex
		signal must not exceed 100 kHz. A query returns <MaxAudioDeviation>, <Ratio>. \n
			:param max_audio_deviation: Maximum audio deviation in Hz Range: 0 Hz to 100 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(max_audio_deviation)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:MADeviation {param}')

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Max_Audio_Deviation: float: Maximum audio deviation in Hz Range: 0 Hz to 100 kHz, Unit: Hz
			- Ratio: float: Maximum audio deviation as percentage of the multiplex deviation Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_float('Max_Audio_Deviation'),
			ArgStruct.scalar_float('Ratio')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Max_Audio_Deviation: float = None
			self.Ratio: float = None

	def get(self) -> GetStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:MADeviation \n
		Snippet: value: GetStruct = driver.source.afRf.generator.modulator.fmStereo.madeviation.get() \n
		Specifies the maximum frequency deviation for the audio signal component of a generated FM stereo multiplex signal. The
		allowed range depends on the frequency deviation of the other signal components. The total deviation of the multiplex
		signal must not exceed 100 kHz. A query returns <MaxAudioDeviation>, <Ratio>. \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:MADeviation?', self.__class__.GetStruct())
