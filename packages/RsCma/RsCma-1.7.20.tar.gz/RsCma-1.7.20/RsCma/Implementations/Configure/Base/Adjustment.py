from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Adjustment:
	"""Adjustment commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("adjustment", core, parent)

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.OscillatorType:
		"""SCPI: CONFigure:BASE:ADJustment:TYPE \n
		Snippet: value: enums.OscillatorType = driver.configure.base.adjustment.get_type_py() \n
		Selects the frequency source to be adjusted. \n
			:return: adj_type: TCXO | OCXO
		"""
		response = self._core.io.query_str('CONFigure:BASE:ADJustment:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.OscillatorType)

	def set_type_py(self, adj_type: enums.OscillatorType) -> None:
		"""SCPI: CONFigure:BASE:ADJustment:TYPE \n
		Snippet: driver.configure.base.adjustment.set_type_py(adj_type = enums.OscillatorType.OCXO) \n
		Selects the frequency source to be adjusted. \n
			:param adj_type: TCXO | OCXO
		"""
		param = Conversions.enum_scalar_to_str(adj_type, enums.OscillatorType)
		self._core.io.write(f'CONFigure:BASE:ADJustment:TYPE {param}')

	def get_value(self) -> float:
		"""SCPI: CONFigure:BASE:ADJustment:VALue \n
		Snippet: value: float = driver.configure.base.adjustment.get_value() \n
		Adjusts the reference frequency. A lower value decreases the frequency. A higher value increases it. \n
			:return: adj_value: Range: 0 to 65535
		"""
		response = self._core.io.query_str('CONFigure:BASE:ADJustment:VALue?')
		return Conversions.str_to_float(response)

	def set_value(self, adj_value: float) -> None:
		"""SCPI: CONFigure:BASE:ADJustment:VALue \n
		Snippet: driver.configure.base.adjustment.set_value(adj_value = 1.0) \n
		Adjusts the reference frequency. A lower value decreases the frequency. A higher value increases it. \n
			:param adj_value: Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(adj_value)
		self._core.io.write(f'CONFigure:BASE:ADJustment:VALue {param}')

	def save(self) -> None:
		"""SCPI: CONFigure:BASE:ADJustment:SAVE \n
		Snippet: driver.configure.base.adjustment.save() \n
		Stores the configured adjustment value. \n
		"""
		self._core.io.write(f'CONFigure:BASE:ADJustment:SAVE')

	def save_with_opc(self, opc_timeout_ms: int = -1) -> None:
		"""SCPI: CONFigure:BASE:ADJustment:SAVE \n
		Snippet: driver.configure.base.adjustment.save_with_opc() \n
		Stores the configured adjustment value. \n
		Same as save, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param opc_timeout_ms: Maximum time to wait in milliseconds, valid only for this call."""
		self._core.io.write_with_opc(f'CONFigure:BASE:ADJustment:SAVE', opc_timeout_ms)
