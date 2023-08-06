from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SpdifRight:
	"""SpdifRight commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spdifRight", core, parent)

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.DigitalToneMode:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:SINRight:TMODe \n
		Snippet: value: enums.DigitalToneMode = driver.configure.afRf.measurement.multiEval.spdifRight.get_tmode() \n
		No command help available \n
			:return: tone_mode: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:SINRight:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.DigitalToneMode)

	def set_tmode(self, tone_mode: enums.DigitalToneMode) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:SINRight:TMODe \n
		Snippet: driver.configure.afRf.measurement.multiEval.spdifRight.set_tmode(tone_mode = enums.DigitalToneMode.DCS) \n
		No command help available \n
			:param tone_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(tone_mode, enums.DigitalToneMode)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:SINRight:TMODe {param}')
