from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("result", core, parent)

	# noinspection PyTypeChecker
	def get_overview(self) -> enums.OverviewType:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:OVERview \n
		Snippet: value: enums.OverviewType = driver.configure.afRf.measurement.multiEval.result.get_overview() \n
		Switches between the 'AF Spectrum' and the 'AF Oscilloscope' diagram if 'AF Spectrum' and 'AF Oscilloscope' are enabled
		results. If no result is enabled, the remote command returns NONE. \n
			:return: type_py: NONE | FFT | OSCilloscope
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:OVERview?')
		return Conversions.str_to_scalar_enum(response, enums.OverviewType)

	def set_overview(self, type_py: enums.OverviewType) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:OVERview \n
		Snippet: driver.configure.afRf.measurement.multiEval.result.set_overview(type_py = enums.OverviewType.FFT) \n
		Switches between the 'AF Spectrum' and the 'AF Oscilloscope' diagram if 'AF Spectrum' and 'AF Oscilloscope' are enabled
		results. If no result is enabled, the remote command returns NONE. \n
			:param type_py: NONE | FFT | OSCilloscope
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.OverviewType)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:OVERview {param}')

	def get_oscilloscope(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:OSCilloscope \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.result.get_oscilloscope() \n
		Enables or disables the measurement of the AF oscilloscope results. \n
			:return: osc_enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:OSCilloscope?')
		return Conversions.str_to_bool(response)

	def set_oscilloscope(self, osc_enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:OSCilloscope \n
		Snippet: driver.configure.afRf.measurement.multiEval.result.set_oscilloscope(osc_enable = False) \n
		Enables or disables the measurement of the AF oscilloscope results. \n
			:param osc_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(osc_enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:OSCilloscope {param}')

	def get_fft(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:FFT \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.result.get_fft() \n
		Enables or disables the measurement of the AF spectrum results. \n
			:return: fft_enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:FFT?')
		return Conversions.str_to_bool(response)

	def set_fft(self, fft_enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:FFT \n
		Snippet: driver.configure.afRf.measurement.multiEval.result.set_fft(fft_enable = False) \n
		Enables or disables the measurement of the AF spectrum results. \n
			:param fft_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(fft_enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:RESult:FFT {param}')
