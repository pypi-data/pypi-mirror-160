from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Uplink:
	"""Uplink commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("uplink", core, parent)

	def get_bcc(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:BCC \n
		Snippet: value: int = driver.configure.afRf.measurement.digital.tetra.uplink.get_bcc() \n
		Defines for the TETRA standard the color code to be signaled from the base station to the DUT. \n
			:return: base_color_code: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:BCC?')
		return Conversions.str_to_int(response)

	def set_bcc(self, base_color_code: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:BCC \n
		Snippet: driver.configure.afRf.measurement.digital.tetra.uplink.set_bcc(base_color_code = 1) \n
		Defines for the TETRA standard the color code to be signaled from the base station to the DUT. \n
			:param base_color_code: No help available
		"""
		param = Conversions.decimal_value_to_str(base_color_code)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:BCC {param}')

	def get_mcc(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:MCC \n
		Snippet: value: int = driver.configure.afRf.measurement.digital.tetra.uplink.get_mcc() \n
		Sets the mobile country code for TETRA. \n
			:return: mcc: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:MCC?')
		return Conversions.str_to_int(response)

	def set_mcc(self, mcc: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:MCC \n
		Snippet: driver.configure.afRf.measurement.digital.tetra.uplink.set_mcc(mcc = 1) \n
		Sets the mobile country code for TETRA. \n
			:param mcc: No help available
		"""
		param = Conversions.decimal_value_to_str(mcc)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:MCC {param}')

	def get_mnc(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:MNC \n
		Snippet: value: int = driver.configure.afRf.measurement.digital.tetra.uplink.get_mnc() \n
		Sets the mobile network code for TETRA. \n
			:return: mnc: No help available
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:MNC?')
		return Conversions.str_to_int(response)

	def set_mnc(self, mnc: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:MNC \n
		Snippet: driver.configure.afRf.measurement.digital.tetra.uplink.set_mnc(mnc = 1) \n
		Sets the mobile network code for TETRA. \n
			:param mnc: No help available
		"""
		param = Conversions.decimal_value_to_str(mnc)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DIGital:TETRa:UPLink:MNC {param}')
