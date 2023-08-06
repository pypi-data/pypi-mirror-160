from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rbw:
	"""Rbw commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rbw", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.RbwFilterType:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:TYPE \n
		Snippet: value: enums.RbwFilterType = driver.configure.gprfMeasurement.spectrum.zeroSpan.rbw.get_type_py() \n
		Selects the resolution filter type for the zero span mode. \n
			:return: rbw_type: GAUSs | BANDpass GAUSs Gaussian filter with configurable bandwidth BANDpass Bandpass filter with 40 MHz bandwidth
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.RbwFilterType)

	def set_type_py(self, rbw_type: enums.RbwFilterType) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:TYPE \n
		Snippet: driver.configure.gprfMeasurement.spectrum.zeroSpan.rbw.set_type_py(rbw_type = enums.RbwFilterType.BANDpass) \n
		Selects the resolution filter type for the zero span mode. \n
			:param rbw_type: GAUSs | BANDpass GAUSs Gaussian filter with configurable bandwidth BANDpass Bandpass filter with 40 MHz bandwidth
		"""
		param = Conversions.enum_scalar_to_str(rbw_type, enums.RbwFilterType)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:TYPE {param}')

	def get_bandpass(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:BANDpass \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.zeroSpan.rbw.get_bandpass() \n
		Sets the resolution bandwidth of the 'Bandpass' filter type in the spectrum measurement. The resolution bandwidth is
		fixed in this software version. \n
			:return: rbw_bandpass: Range: 40 MHz to 40 MHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:BANDpass?')
		return Conversions.str_to_float(response)

	def set_bandpass(self, rbw_bandpass: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:BANDpass \n
		Snippet: driver.configure.gprfMeasurement.spectrum.zeroSpan.rbw.set_bandpass(rbw_bandpass = 1.0) \n
		Sets the resolution bandwidth of the 'Bandpass' filter type in the spectrum measurement. The resolution bandwidth is
		fixed in this software version. \n
			:param rbw_bandpass: Range: 40 MHz to 40 MHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(rbw_bandpass)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:BANDpass {param}')

	def get_gauss(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:GAUSs \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.zeroSpan.rbw.get_gauss() \n
		Selects the bandwidth of the Gaussian resolution filter for the zero span mode. To use this filter, configure also method
		RsCma.Configure.GprfMeasurement.Spectrum.ZeroSpan.Rbw.typePy. \n
			:return: rbw: You can enter values between 100 Hz and 10 MHz. The setting is rounded to the closest of the following values: 100 / 200 / 300 / 500 Hz 1 / 2 / 3 / 5 / 10 / 20 / 30 / 50 / 100 / 200 / 300 / 500 kHz 1 / 2 / 3 / 5 / 10 MHz Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:GAUSs?')
		return Conversions.str_to_float(response)

	def set_gauss(self, rbw: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:GAUSs \n
		Snippet: driver.configure.gprfMeasurement.spectrum.zeroSpan.rbw.set_gauss(rbw = 1.0) \n
		Selects the bandwidth of the Gaussian resolution filter for the zero span mode. To use this filter, configure also method
		RsCma.Configure.GprfMeasurement.Spectrum.ZeroSpan.Rbw.typePy. \n
			:param rbw: You can enter values between 100 Hz and 10 MHz. The setting is rounded to the closest of the following values: 100 / 200 / 300 / 500 Hz 1 / 2 / 3 / 5 / 10 / 20 / 30 / 50 / 100 / 200 / 300 / 500 kHz 1 / 2 / 3 / 5 / 10 MHz Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(rbw)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:RBW:GAUSs {param}')
