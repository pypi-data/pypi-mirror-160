from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Attenuation:
	"""Attenuation commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("attenuation", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:BASE:ATTenuation:ENABle \n
		Snippet: value: bool = driver.configure.base.attenuation.get_enable() \n
		Enables or disables the internal 17 dB attenuator of the RF COM connector. \n
			:return: atten_enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BASE:ATTenuation:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, atten_enable: bool) -> None:
		"""SCPI: CONFigure:BASE:ATTenuation:ENABle \n
		Snippet: driver.configure.base.attenuation.set_enable(atten_enable = False) \n
		Enables or disables the internal 17 dB attenuator of the RF COM connector. \n
			:param atten_enable: OFF | ON
		"""
		param = Conversions.bool_to_str(atten_enable)
		self._core.io.write(f'CONFigure:BASE:ATTenuation:ENABle {param}')

	def get_awarning(self) -> bool:
		"""SCPI: CONFigure:BASE:ATTenuation:AWARning \n
		Snippet: value: bool = driver.configure.base.attenuation.get_awarning() \n
		Enables or disables an audible warning, to be played if the RF protection circuit is activated. \n
			:return: awarning: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:BASE:ATTenuation:AWARning?')
		return Conversions.str_to_bool(response)

	def set_awarning(self, awarning: bool) -> None:
		"""SCPI: CONFigure:BASE:ATTenuation:AWARning \n
		Snippet: driver.configure.base.attenuation.set_awarning(awarning = False) \n
		Enables or disables an audible warning, to be played if the RF protection circuit is activated. \n
			:param awarning: OFF | ON
		"""
		param = Conversions.bool_to_str(awarning)
		self._core.io.write(f'CONFigure:BASE:ATTenuation:AWARning {param}')
