from typing import List

from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	def reset(self) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:FREQuency:RESet \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dtmf.frequency.reset() \n
		Triggers a reset of user-defined frequency values to the default frequency values of the DTMF standard. \n
		"""
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:FREQuency:RESet')

	def reset_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:FREQuency:RESet \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dtmf.frequency.reset_with_opc() \n
		Triggers a reset of user-defined frequency values to the default frequency values of the DTMF standard. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:FREQuency:RESet', opc_timeout_ms)

	def get_value(self) -> List[float]:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:FREQuency \n
		Snippet: value: List[float] = driver.configure.afRf.measurement.multiEval.tones.dtmf.frequency.get_value() \n
		Configures the user-defined tone table for DTMF. To enable the table, see method RsCma.Configure.AfRf.Measurement.
		MultiEval.Tones.Dtmf.UserDefined.enable. \n
			:return: frequency: Comma-separated list of up to 8 frequencies You can specify fewer than 8 values to configure only the beginning of the tone table. Range: see table , Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_float_list('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:FREQuency?')
		return response

	def set_value(self, frequency: List[float]) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:FREQuency \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.dtmf.frequency.set_value(frequency = [1.1, 2.2, 3.3]) \n
		Configures the user-defined tone table for DTMF. To enable the table, see method RsCma.Configure.AfRf.Measurement.
		MultiEval.Tones.Dtmf.UserDefined.enable. \n
			:param frequency: Comma-separated list of up to 8 frequencies You can specify fewer than 8 values to configure only the beginning of the tone table. Range: see table , Unit: Hz
		"""
		param = Conversions.list_to_csv_str(frequency)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:DTMF:FREQuency {param}')
