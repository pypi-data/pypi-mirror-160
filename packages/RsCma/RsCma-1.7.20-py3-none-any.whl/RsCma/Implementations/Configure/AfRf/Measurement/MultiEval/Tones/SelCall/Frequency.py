from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........Internal.Types import DataType
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def set(self, standard: enums.SelCallStandard, frequency: List[float]) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:FREQuency \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.selCall.frequency.set(standard = enums.SelCallStandard.CCIR, frequency = [1.1, 2.2, 3.3]) \n
		Configures the user-defined tone table for a SelCall standard. To enable the table, see method RsCma.Configure.AfRf.
		Measurement.MultiEval.Tones.SelCall.UserDefined.enable. \n
			:param standard: CCIR | EEA | EIA | ZVEI1 | ZVEI2 | ZVEI3 | DZVei | PZVei Selects the SelCall standard
			:param frequency: Comma-separated list of up to 16 frequencies, for digit 0 to F You can specify fewer than 16 values to configure only the beginning of the tone table. The *RST values and ranges depend on the SelCall standard and on the digit. The ranges are approximately: default frequency minus 5% to default frequency plus 5%. Unit: Hz
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('standard', standard, DataType.Enum, enums.SelCallStandard), ArgSingle.as_open_list('frequency', frequency, DataType.FloatList, None))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:FREQuency {param}'.rstrip())

	def get(self, standard: enums.SelCallStandard) -> List[float]:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:FREQuency \n
		Snippet: value: List[float] = driver.configure.afRf.measurement.multiEval.tones.selCall.frequency.get(standard = enums.SelCallStandard.CCIR) \n
		Configures the user-defined tone table for a SelCall standard. To enable the table, see method RsCma.Configure.AfRf.
		Measurement.MultiEval.Tones.SelCall.UserDefined.enable. \n
			:param standard: CCIR | EEA | EIA | ZVEI1 | ZVEI2 | ZVEI3 | DZVei | PZVei Selects the SelCall standard
			:return: frequency: Comma-separated list of up to 16 frequencies, for digit 0 to F You can specify fewer than 16 values to configure only the beginning of the tone table. The *RST values and ranges depend on the SelCall standard and on the digit. The ranges are approximately: default frequency minus 5% to default frequency plus 5%. Unit: Hz"""
		param = Conversions.enum_scalar_to_str(standard, enums.SelCallStandard)
		response = self._core.io.query_bin_or_ascii_float_list(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:FREQuency? {param}')
		return response

	def reset(self) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:FREQuency:RESet \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.selCall.frequency.reset() \n
		Triggers a reset of user-defined frequency values to the default frequency values of the selective-calling standard. \n
		"""
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:FREQuency:RESet')

	def reset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:FREQuency:RESet \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.selCall.frequency.reset_with_opc() \n
		Triggers a reset of user-defined frequency values to the default frequency values of the selective-calling standard. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SELCall:FREQuency:RESet', opc_timeout_ms)
