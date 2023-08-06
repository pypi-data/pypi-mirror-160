from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voip:
	"""Voip commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("voip", core, parent)

	# noinspection PyTypeChecker
	def get_xdivision(self) -> enums.Xdivision:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:VOIP:XDIVision \n
		Snippet: value: enums.Xdivision = driver.configure.afRf.measurement.multiEval.oscilloscope.voip.get_xdivision() \n
		Configures the x-axis division of the oscilloscope result diagram. The measurement time equals 10 divisions. \n
			:return: xdivision: U1 | U2 | U5 | U10 | U20 | U50 | U100 | U200 | U500 | M1 | M2 | M5 | M10 | M20 | M50 | M100 | M200 | M500 | S1 Duration of one division. The letters indicate the unit as follows: U = µs, M=ms, S=s Example: U20 = 20 µs/division
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:VOIP:XDIVision?')
		return Conversions.str_to_scalar_enum(response, enums.Xdivision)

	def set_xdivision(self, xdivision: enums.Xdivision) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:VOIP:XDIVision \n
		Snippet: driver.configure.afRf.measurement.multiEval.oscilloscope.voip.set_xdivision(xdivision = enums.Xdivision.M1) \n
		Configures the x-axis division of the oscilloscope result diagram. The measurement time equals 10 divisions. \n
			:param xdivision: U1 | U2 | U5 | U10 | U20 | U50 | U100 | U200 | U500 | M1 | M2 | M5 | M10 | M20 | M50 | M100 | M200 | M500 | S1 Duration of one division. The letters indicate the unit as follows: U = µs, M=ms, S=s Example: U20 = 20 µs/division
		"""
		param = Conversions.enum_scalar_to_str(xdivision, enums.Xdivision)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:VOIP:XDIVision {param}')

	def get_mtime(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:VOIP:MTIMe \n
		Snippet: value: float = driver.configure.afRf.measurement.multiEval.oscilloscope.voip.get_mtime() \n
		Query the measurement time per input path. The measurement time is the time covered by one complete result trace (10
		x-axis divisions) . \n
			:return: meas_time: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:VOIP:MTIMe?')
		return Conversions.str_to_float(response)

	def set_mtime(self, meas_time: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:VOIP:MTIMe \n
		Snippet: driver.configure.afRf.measurement.multiEval.oscilloscope.voip.set_mtime(meas_time = 1.0) \n
		Query the measurement time per input path. The measurement time is the time covered by one complete result trace (10
		x-axis divisions) . \n
			:param meas_time: Unit: s
		"""
		param = Conversions.decimal_value_to_str(meas_time)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:VOIP:MTIMe {param}')
