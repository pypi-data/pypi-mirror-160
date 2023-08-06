from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FilterPy:
	"""FilterPy commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("filterPy", core, parent)

	# noinspection PyTypeChecker
	def get_bandwidth(self) -> enums.BandpassFilter:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:FILTer:BWIDth \n
		Snippet: value: enums.BandpassFilter = driver.configure.afRf.measurement.multiEval.filterPy.get_bandwidth() \n
		Configures the bandwidth of the bandpass filter in the RF input path. \n
			:return: bandpass: F8330 | F25K | F50K | F01M | F05M Bandwidth 8330 Hz, 25 kHz, 50 kHz, 0.1 MHz, 0.5 MHz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:FILTer:BWIDth?')
		return Conversions.str_to_scalar_enum(response, enums.BandpassFilter)

	def set_bandwidth(self, bandpass: enums.BandpassFilter) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:FILTer:BWIDth \n
		Snippet: driver.configure.afRf.measurement.multiEval.filterPy.set_bandwidth(bandpass = enums.BandpassFilter.F01M) \n
		Configures the bandwidth of the bandpass filter in the RF input path. \n
			:param bandpass: F8330 | F25K | F50K | F01M | F05M Bandwidth 8330 Hz, 25 kHz, 50 kHz, 0.1 MHz, 0.5 MHz
		"""
		param = Conversions.enum_scalar_to_str(bandpass, enums.BandpassFilter)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:FILTer:BWIDth {param}')
