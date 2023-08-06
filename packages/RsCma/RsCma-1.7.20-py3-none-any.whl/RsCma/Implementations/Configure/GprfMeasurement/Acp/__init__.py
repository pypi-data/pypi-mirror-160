from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Acp:
	"""Acp commands group definition. 14 total commands, 2 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("acp", core, parent)

	@property
	def obw(self):
		"""obw commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_obw'):
			from .Obw import Obw
			self._obw = Obw(self._core, self._cmd_group)
		return self._obw

	@property
	def limit(self):
		"""limit commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_limit'):
			from .Limit import Limit
			self._limit = Limit(self._core, self._cmd_group)
		return self._limit

	def get_mo_exception(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:MOEXception \n
		Snippet: value: bool = driver.configure.gprfMeasurement.acp.get_mo_exception() \n
		Specifies whether measurement results that the R&S CMA180 identifies as faulty or inaccurate are rejected. \n
			:return: meas_on_exception: OFF | ON OFF Faulty results are rejected ON Results are never rejected
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:ACP:MOEXception?')
		return Conversions.str_to_bool(response)

	def set_mo_exception(self, meas_on_exception: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:MOEXception \n
		Snippet: driver.configure.gprfMeasurement.acp.set_mo_exception(meas_on_exception = False) \n
		Specifies whether measurement results that the R&S CMA180 identifies as faulty or inaccurate are rejected. \n
			:param meas_on_exception: OFF | ON OFF Faulty results are rejected ON Results are never rejected
		"""
		param = Conversions.bool_to_str(meas_on_exception)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:MOEXception {param}')

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:TOUT \n
		Snippet: value: float = driver.configure.gprfMeasurement.acp.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: tcd_timeout: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:ACP:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_timeout: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:TOUT \n
		Snippet: driver.configure.gprfMeasurement.acp.set_timeout(tcd_timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param tcd_timeout: Unit: s
		"""
		param = Conversions.decimal_value_to_str(tcd_timeout)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:TOUT {param}')

	# noinspection PyTypeChecker
	def get_repetition(self) -> enums.Repeat:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:REPetition \n
		Snippet: value: enums.Repeat = driver.configure.gprfMeasurement.acp.get_repetition() \n
		Selects whether the measurement is repeated continuously or not. \n
			:return: repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:ACP:REPetition?')
		return Conversions.str_to_scalar_enum(response, enums.Repeat)

	def set_repetition(self, repetition: enums.Repeat) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:REPetition \n
		Snippet: driver.configure.gprfMeasurement.acp.set_repetition(repetition = enums.Repeat.CONTinuous) \n
		Selects whether the measurement is repeated continuously or not. \n
			:param repetition: SINGleshot | CONTinuous SINGleshot Single-shot measurement, stopped after one measurement cycle CONTinuous Continuous measurement, running until explicitly terminated
		"""
		param = Conversions.enum_scalar_to_str(repetition, enums.Repeat)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:REPetition {param}')

	def get_rcoupling(self) -> bool:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:RCOupling \n
		Snippet: value: bool = driver.configure.gprfMeasurement.acp.get_rcoupling() \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:return: repetition_coupl: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:ACP:RCOupling?')
		return Conversions.str_to_bool(response)

	def set_rcoupling(self, repetition_coupl: bool) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:RCOupling \n
		Snippet: driver.configure.gprfMeasurement.acp.set_rcoupling(repetition_coupl = False) \n
		Couples the repetition mode (single shot or continuous) of all measurements. \n
			:param repetition_coupl: OFF | ON
		"""
		param = Conversions.bool_to_str(repetition_coupl)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:RCOupling {param}')

	def get_scount(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:SCOunt \n
		Snippet: value: int = driver.configure.gprfMeasurement.acp.get_scount() \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval delivers one set of
		'Current' results. \n
			:return: statistic_count: Range: 1 to 1000
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:ACP:SCOunt?')
		return Conversions.str_to_int(response)

	def set_scount(self, statistic_count: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:SCOunt \n
		Snippet: driver.configure.gprfMeasurement.acp.set_scount(statistic_count = 1) \n
		Specifies the number of measurement intervals per measurement cycle. One measurement interval delivers one set of
		'Current' results. \n
			:param statistic_count: Range: 1 to 1000
		"""
		param = Conversions.decimal_value_to_str(statistic_count)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:SCOunt {param}')

	def get_cspace(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:CSPace \n
		Snippet: value: int = driver.configure.gprfMeasurement.acp.get_cspace() \n
		Defines the channel spacing, that is the center frequency difference of two adjacent channels. \n
			:return: channel_space: Range: 100 Hz to 4 MHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:ACP:CSPace?')
		return Conversions.str_to_int(response)

	def set_cspace(self, channel_space: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:CSPace \n
		Snippet: driver.configure.gprfMeasurement.acp.set_cspace(channel_space = 1) \n
		Defines the channel spacing, that is the center frequency difference of two adjacent channels. \n
			:param channel_space: Range: 100 Hz to 4 MHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(channel_space)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:CSPace {param}')

	def get_mbwidth(self) -> List[int]:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:MBWidth \n
		Snippet: value: List[int] = driver.configure.gprfMeasurement.acp.get_mbwidth() \n
		Defines the width of the measurement filter used to measure the channel power. The maximum allowed value is limited by
		the channel spacing, see method RsCma.Configure.GprfMeasurement.Acp.cspace. \n
			:return: meas_band_width: Range: 100 Hz to ChannelSpace, Unit: Hz
		"""
		response = self._core.io.query_bin_or_ascii_int_list('CONFigure:GPRF:MEASurement<Instance>:ACP:MBWidth?')
		return response

	def set_mbwidth(self, meas_band_width: List[int]) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:MBWidth \n
		Snippet: driver.configure.gprfMeasurement.acp.set_mbwidth(meas_band_width = [1, 2, 3]) \n
		Defines the width of the measurement filter used to measure the channel power. The maximum allowed value is limited by
		the channel spacing, see method RsCma.Configure.GprfMeasurement.Acp.cspace. \n
			:param meas_band_width: Range: 100 Hz to ChannelSpace, Unit: Hz
		"""
		param = Conversions.list_to_csv_str(meas_band_width)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:MBWidth {param}')

	# noinspection PyTypeChecker
	def get_offset(self) -> enums.AcpOffset:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:OFFSet \n
		Snippet: value: enums.AcpOffset = driver.configure.gprfMeasurement.acp.get_offset() \n
		Specifies an offset, moving the designated channel center frequency relative to the RF carrier center frequency. \n
			:return: offset: NONE | USB | LSB NONE No offset, for example for FM, PM, AM USB Positive offset, for USB modulation LSB Negative offset, for LSB modulation
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:ACP:OFFSet?')
		return Conversions.str_to_scalar_enum(response, enums.AcpOffset)

	def set_offset(self, offset: enums.AcpOffset) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:OFFSet \n
		Snippet: driver.configure.gprfMeasurement.acp.set_offset(offset = enums.AcpOffset.LSB) \n
		Specifies an offset, moving the designated channel center frequency relative to the RF carrier center frequency. \n
			:param offset: NONE | USB | LSB NONE No offset, for example for FM, PM, AM USB Positive offset, for USB modulation LSB Negative offset, for LSB modulation
		"""
		param = Conversions.enum_scalar_to_str(offset, enums.AcpOffset)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:ACP:OFFSet {param}')

	def clone(self) -> 'Acp':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Acp(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
