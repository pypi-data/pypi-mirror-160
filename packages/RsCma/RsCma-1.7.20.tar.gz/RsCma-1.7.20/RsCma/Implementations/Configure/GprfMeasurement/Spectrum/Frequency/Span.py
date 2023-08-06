from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Span:
	"""Span commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("span", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SpanMode:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:SPAN:MODE \n
		Snippet: value: enums.SpanMode = driver.configure.gprfMeasurement.spectrum.frequency.span.get_mode() \n
		Selects the measurement mode. \n
			:return: span_mode: FSWeep | ZSPan FSWeep Frequency sweep mode ZSPan Zero span mode
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:SPAN:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SpanMode)

	def set_mode(self, span_mode: enums.SpanMode) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:SPAN:MODE \n
		Snippet: driver.configure.gprfMeasurement.spectrum.frequency.span.set_mode(span_mode = enums.SpanMode.FSWeep) \n
		Selects the measurement mode. \n
			:param span_mode: FSWeep | ZSPan FSWeep Frequency sweep mode ZSPan Zero span mode
		"""
		param = Conversions.enum_scalar_to_str(span_mode, enums.SpanMode)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:SPAN:MODE {param}')

	def get_value(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:SPAN \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.frequency.span.get_value() \n
		Specifies the frequency span for the frequency sweep mode. \n
			:return: frequency_span: Range: 1000 Hz to 2.999901 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:SPAN?')
		return Conversions.str_to_float(response)

	def set_value(self, frequency_span: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:SPAN \n
		Snippet: driver.configure.gprfMeasurement.spectrum.frequency.span.set_value(frequency_span = 1.0) \n
		Specifies the frequency span for the frequency sweep mode. \n
			:param frequency_span: Range: 1000 Hz to 2.999901 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency_span)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:FREQuency:SPAN {param}')
