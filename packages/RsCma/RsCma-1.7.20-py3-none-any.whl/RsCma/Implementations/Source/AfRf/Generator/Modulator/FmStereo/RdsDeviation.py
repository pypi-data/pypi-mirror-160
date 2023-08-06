from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RdsDeviation:
	"""RdsDeviation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rdsDeviation", core, parent)

	def set(self, rds_deviation: float) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:RDSDeviation \n
		Snippet: driver.source.afRf.generator.modulator.fmStereo.rdsDeviation.set(rds_deviation = 1.0) \n
		Specifies the maximum frequency deviation for the RDS signal component of a generated FM stereo multiplex signal.
		The allowed range depends on the frequency deviation of the other signal components. The total deviation of the multiplex
		signal must not exceed 100 kHz. A query returns <RDSDeviation>, <Ratio>. \n
			:param rds_deviation: Maximum RDS deviation in Hz Range: 0 Hz to 10 kHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(rds_deviation)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:RDSDeviation {param}')

	# noinspection PyTypeChecker
	class GetStruct(StructBase):
		"""Response structure. Fields: \n
			- Rds_Deviation: float: Maximum RDS deviation in Hz Range: 0 Hz to 10 kHz, Unit: Hz
			- Ratio: float: Maximum RDS deviation as percentage of the multiplex deviation Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_float('Rds_Deviation'),
			ArgStruct.scalar_float('Ratio')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rds_Deviation: float = None
			self.Ratio: float = None

	def get(self) -> GetStruct:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:RDSDeviation \n
		Snippet: value: GetStruct = driver.source.afRf.generator.modulator.fmStereo.rdsDeviation.get() \n
		Specifies the maximum frequency deviation for the RDS signal component of a generated FM stereo multiplex signal.
		The allowed range depends on the frequency deviation of the other signal components. The total deviation of the multiplex
		signal must not exceed 100 kHz. A query returns <RDSDeviation>, <Ratio>. \n
			:return: structure: for return value, see the help for GetStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:AFRF:GENerator<Instance>:MODulator:FMSTereo:RDSDeviation?', self.__class__.GetStruct())
