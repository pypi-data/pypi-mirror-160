from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("demodulation", core, parent)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.DigitalToneMode:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DEModulation:MODE \n
		Snippet: value: enums.DigitalToneMode = driver.configure.afRf.measurement.multiEval.tones.demodulation.get_mode() \n
		Selects a dialing tone mode for the RF input path. \n
			:return: tone_mode: NONE | SELCall | DTMF | FDIA | SCAL | DCS None, SelCall, DTMF, free dialing, SELCAL, DCS
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DEModulation:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DigitalToneMode)

	def set_mode(self, tone_mode: enums.DigitalToneMode) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DEModulation:MODE \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.demodulation.set_mode(tone_mode = enums.DigitalToneMode.DCS) \n
		Selects a dialing tone mode for the RF input path. \n
			:param tone_mode: NONE | SELCall | DTMF | FDIA | SCAL | DCS None, SelCall, DTMF, free dialing, SELCAL, DCS
		"""
		param = Conversions.enum_scalar_to_str(tone_mode, enums.DigitalToneMode)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DEModulation:MODE {param}')
