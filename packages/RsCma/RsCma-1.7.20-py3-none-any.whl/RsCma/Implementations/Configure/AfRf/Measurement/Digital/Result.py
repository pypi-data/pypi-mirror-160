from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Result:
	"""Result commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("result", core, parent)

	def get_ber(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:RESult:BER \n
		Snippet: value: bool = driver.configure.afRf.measurement.digital.result.get_ber() \n
		Enables or disables the indication of the BER measurement results. \n
			:return: ber_enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:RESult:BER?')
		return Conversions.str_to_bool(response)

	def set_ber(self, ber_enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:RESult:BER \n
		Snippet: driver.configure.afRf.measurement.digital.result.set_ber(ber_enable = False) \n
		Enables or disables the indication of the BER measurement results. \n
			:param ber_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(ber_enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:RESult:BER {param}')
