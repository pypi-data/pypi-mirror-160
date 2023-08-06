from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rsquelch:
	"""Rsquelch commands group definition. 3 total commands, 0 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rsquelch", core, parent)

	def get_so_time(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:SOTime \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.rsquelch.get_so_time() \n
		Defines the time period for which the audio signal has to be continuously unmuted (or muted) after the DUT has switched
		off (or on) the squelch. The search routine only returns a positive result for the squelch level if the audio signal
		quality is detected as continuously high (or low) over that period. \n
			:return: sq_observ_time: Range: 1 s to 20 s, Unit: s
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:SOTime?')
		return Conversions.str_to_float(response)

	def set_so_time(self, sq_observ_time: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:SOTime \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.rsquelch.set_so_time(sq_observ_time = 1.0) \n
		Defines the time period for which the audio signal has to be continuously unmuted (or muted) after the DUT has switched
		off (or on) the squelch. The search routine only returns a positive result for the squelch level if the audio signal
		quality is detected as continuously high (or low) over that period. \n
			:param sq_observ_time: Range: 1 s to 20 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(sq_observ_time)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:SOTime {param}')

	def get_lvl_tolerance(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:LVLTolerance \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.rsquelch.get_lvl_tolerance() \n
		Defines the maximum deviation from the measured average audio signal level during the 'Squelch Observation Time' when the
		squelch is switched off at the DUT. \n
			:return: tolerance: Unit: dB
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:LVLTolerance?')
		return Conversions.str_to_float(response)

	def set_lvl_tolerance(self, tolerance: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:LVLTolerance \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.rsquelch.set_lvl_tolerance(tolerance = 1.0) \n
		Defines the maximum deviation from the measured average audio signal level during the 'Squelch Observation Time' when the
		squelch is switched off at the DUT. \n
			:param tolerance: Unit: dB
		"""
		param = Conversions.decimal_value_to_str(tolerance)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:LVLTolerance {param}')

	# noinspection PyTypeChecker
	def get_extent(self) -> enums.SearchExtent:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:EXTent \n
		Snippet: value: enums.SearchExtent = driver.configure.afRf.measurement.searchRoutines.rsquelch.get_extent() \n
		Defines the extent of the 'RX Squelch' search routine measurement. \n
			:return: search_extent: FULL | OFFLevel | ONLevel FULL Determines the squelch switch-on level and switch-off level. OFFLevel Determines the squelch switch-off level. ONLevel Determines the squelch switch-on level.
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:EXTent?')
		return Conversions.str_to_scalar_enum(response, enums.SearchExtent)

	def set_extent(self, search_extent: enums.SearchExtent) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:EXTent \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.rsquelch.set_extent(search_extent = enums.SearchExtent.FULL) \n
		Defines the extent of the 'RX Squelch' search routine measurement. \n
			:param search_extent: FULL | OFFLevel | ONLevel FULL Determines the squelch switch-on level and switch-off level. OFFLevel Determines the squelch switch-off level. ONLevel Determines the squelch switch-on level.
		"""
		param = Conversions.enum_scalar_to_str(search_extent, enums.SearchExtent)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:RSQuelch:EXTent {param}')
