from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pdeviation:
	"""Pdeviation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pdeviation", core, parent)

	def set(self, max_pilot_deviation: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:PDEViation \n
		Snippet: driver.source.afRf.generator.modulator.fmStereo.pdeviation.set(max_pilot_deviation = 1.0) \n
		Specifies the maximum frequency deviation for the pilot tone of a generated FM stereo multiplex signal. The allowed range
		depends on the frequency deviation of the other signal components. The total deviation of the multiplex signal must not
		exceed 100 kHz. A query returns <MaxPilotDeviation>, <Ratio>. \n
			:param max_pilot_deviation: Maximum pilot deviation in Hz Range: 0 Hz to 10 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(max_pilot_deviation)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:PDEViation {param}')

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Max_Pilot_Deviation: float: Maximum pilot deviation in Hz Range: 0 Hz to 10 kHz, Unit: Hz
			- Ratio: float: Maximum pilot deviation as percentage of the multiplex deviation Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_float('Max_Pilot_Deviation'),
			ArgStruct.scalar_float('Ratio')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Max_Pilot_Deviation: float = None
			self.Ratio: float = None

	def get(self) -> GetStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:PDEViation \n
		Snippet: value: GetStruct = driver.source.afRf.generator.modulator.fmStereo.pdeviation.get() \n
		Specifies the maximum frequency deviation for the pilot tone of a generated FM stereo multiplex signal. The allowed range
		depends on the frequency deviation of the other signal components. The total deviation of the multiplex signal must not
		exceed 100 kHz. A query returns <MaxPilotDeviation>, <Ratio>. \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:PDEViation?', self.__class__.GetStruct())
