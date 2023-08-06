from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Zbox:
	"""Zbox commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("zbox", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:BASE:ZBOX:ENABle \n
		Snippet: value: bool = driver.configure.base.zbox.get_enable() \n
		No command help available \n
			:return: enable: No help available
		"""
		response = self._core.io.query_str('CONFigure:BASE:ZBOX:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, enable: bool) -> None:
		"""SCPI: CONFigure:BASE:ZBOX:ENABle \n
		Snippet: driver.configure.base.zbox.set_enable(enable = False) \n
		No command help available \n
			:param enable: No help available
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:BASE:ZBOX:ENABle {param}')

	# noinspection PyTypeChecker
	def get_impedance(self) -> enums.Impedance:
		"""SCPI: CONFigure:BASE:ZBOX:IMPedance \n
		Snippet: value: enums.Impedance = driver.configure.base.zbox.get_impedance() \n
		No command help available \n
			:return: impedance: No help available
		"""
		response = self._core.io.query_str('CONFigure:BASE:ZBOX:IMPedance?')
		return Conversions.str_to_scalar_enum(response, enums.Impedance)

	def set_impedance(self, impedance: enums.Impedance) -> None:
		"""SCPI: CONFigure:BASE:ZBOX:IMPedance \n
		Snippet: driver.configure.base.zbox.set_impedance(impedance = enums.Impedance.IHOL) \n
		No command help available \n
			:param impedance: No help available
		"""
		param = Conversions.enum_scalar_to_str(impedance, enums.Impedance)
		self._core.io.write(f'CONFigure:BASE:ZBOX:IMPedance {param}')
