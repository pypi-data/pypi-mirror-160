from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fft:
	"""Fft commands group definition. 5 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("fft", core, parent)

	@property
	def marker(self):
		"""marker commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Marker import Marker
			self._marker = Marker(self._core, self._cmd_group)
		return self._marker

	# noinspection PyTypeChecker
	def get_span(self) -> enums.FftSpan:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:SPAN \n
		Snippet: value: enums.FftSpan = driver.configure.afRf.measurement.multiEval.fft.get_span() \n
		No command help available \n
			:return: span: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:SPAN?')
		return Conversions.str_to_scalar_enum(response, enums.FftSpan)

	def set_span(self, span: enums.FftSpan) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:SPAN \n
		Snippet: driver.configure.afRf.measurement.multiEval.fft.set_span(span = enums.FftSpan.SP1) \n
		No command help available \n
			:param span: No help available
		"""
		param = Conversions.enum_scalar_to_str(span, enums.FftSpan)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:SPAN {param}')

	# noinspection PyTypeChecker
	def get_length(self) -> enums.FftLength:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:LENGth \n
		Snippet: value: enums.FftLength = driver.configure.afRf.measurement.multiEval.fft.get_length() \n
		No command help available \n
			:return: length: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:LENGth?')
		return Conversions.str_to_scalar_enum(response, enums.FftLength)

	def set_length(self, length: enums.FftLength) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:LENGth \n
		Snippet: driver.configure.afRf.measurement.multiEval.fft.set_length(length = enums.FftLength.F16K) \n
		No command help available \n
			:param length: No help available
		"""
		param = Conversions.enum_scalar_to_str(length, enums.FftLength)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:LENGth {param}')

	# noinspection PyTypeChecker
	def get_window(self) -> enums.FftWindowType:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:WINDow \n
		Snippet: value: enums.FftWindowType = driver.configure.afRf.measurement.multiEval.fft.get_window() \n
		Selects the window function to be applied before the fast Fourier transformation. \n
			:return: type_py: RECTangle | HAMMing | HANN | BLHA | FLTP RECTangle, HAMMing, HANN Rectangular / Hamming / Hann window BLHA Blackman-Harris window FLTP Flat-Top window
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:WINDow?')
		return Conversions.str_to_scalar_enum(response, enums.FftWindowType)

	def set_window(self, type_py: enums.FftWindowType) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:WINDow \n
		Snippet: driver.configure.afRf.measurement.multiEval.fft.set_window(type_py = enums.FftWindowType.BLHA) \n
		Selects the window function to be applied before the fast Fourier transformation. \n
			:param type_py: RECTangle | HAMMing | HANN | BLHA | FLTP RECTangle, HAMMing, HANN Rectangular / Hamming / Hann window BLHA Blackman-Harris window FLTP Flat-Top window
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.FftWindowType)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:FFT:WINDow {param}')

	def clone(self) -> 'Fft':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fft(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
