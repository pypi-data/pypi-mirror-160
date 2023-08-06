from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class IqRecorder:
	"""IqRecorder commands group definition. 12 total commands, 2 Subgroups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("iqRecorder", core, parent)

	@property
	def filterPy(self):
		"""filterPy commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._cmd_group)
		return self._filterPy

	@property
	def capture(self):
		"""capture commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_capture'):
			from .Capture import Capture
			self._capture = Capture(self._core, self._cmd_group)
		return self._capture

	def get_toffset(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOFFset \n
		Snippet: value: int = driver.configure.gprfMeasurement.iqRecorder.get_toffset() \n
		No command help available \n
			:return: trigger_offset: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOFFset?')
		return Conversions.str_to_int(response)

	def set_toffset(self, trigger_offset: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOFFset \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.set_toffset(trigger_offset = 1) \n
		No command help available \n
			:param trigger_offset: No help available
		"""
		param = Conversions.decimal_value_to_str(trigger_offset)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOFFset {param}')

	def get_samples(self) -> int:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:SAMPles \n
		Snippet: value: int = driver.configure.gprfMeasurement.iqRecorder.get_samples() \n
		No command help available \n
			:return: samples: No help available
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:SAMPles?')
		return Conversions.str_to_int(response)

	def set_samples(self, samples: int) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:SAMPles \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.set_samples(samples = 1) \n
		No command help available \n
			:param samples: No help available
		"""
		param = Conversions.decimal_value_to_str(samples)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:SAMPles {param}')

	def get_timeout(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOUT \n
		Snippet: value: float = driver.configure.gprfMeasurement.iqRecorder.get_timeout() \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:return: tcd_timeout: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOUT?')
		return Conversions.str_to_float(response)

	def set_timeout(self, tcd_timeout: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOUT \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.set_timeout(tcd_timeout = 1.0) \n
		Defines a timeout for the measurement. The timer is started when the measurement is initiated via a READ or INIT command.
		It is not started if the measurement is initiated via the graphical user interface. The timer is reset after the first
		measurement cycle. If the first measurement cycle has not been completed when the timer expires, the measurement is
		stopped and the reliability indicator is set to 1. Still running READ, FETCh or CALCulate commands are completed,
		returning the available results. At least for some results, there are no values at all or the statistical depth has not
		been reached. A timeout of 0 s corresponds to an infinite measurement timeout. \n
			:param tcd_timeout: Unit: s
		"""
		param = Conversions.decimal_value_to_str(tcd_timeout)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:TOUT {param}')

	def get_ratio(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:RATio \n
		Snippet: value: float = driver.configure.gprfMeasurement.iqRecorder.get_ratio() \n
		Defines the sample ratio and thus the sample rate (<sample rate> = <sample ratio> * <max sample rate>) . \n
			:return: ratio: Range: 0.1 to 1
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:RATio?')
		return Conversions.str_to_float(response)

	def set_ratio(self, ratio: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:RATio \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.set_ratio(ratio = 1.0) \n
		Defines the sample ratio and thus the sample rate (<sample rate> = <sample ratio> * <max sample rate>) . \n
			:param ratio: Range: 0.1 to 1
		"""
		param = Conversions.decimal_value_to_str(ratio)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:RATio {param}')

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.IqFormat:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FORMat \n
		Snippet: value: enums.IqFormat = driver.configure.gprfMeasurement.iqRecorder.get_format_py() \n
		Selects a coordinate system for representation of the measurement results. \n
			:return: format_py: IQ | RPHI IQ Cartesian coordinates (I- and Q-axis) RPHI Polar coordinates (radius and angle)
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.IqFormat)

	def set_format_py(self, format_py: enums.IqFormat) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FORMat \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.set_format_py(format_py = enums.IqFormat.IQ) \n
		Selects a coordinate system for representation of the measurement results. \n
			:param format_py: IQ | RPHI IQ Cartesian coordinates (I- and Q-axis) RPHI Polar coordinates (radius and angle)
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.IqFormat)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:FORMat {param}')

	# noinspection PyTypeChecker
	def get_munit(self) -> enums.MagnitudeUnit:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MUNit \n
		Snippet: value: enums.MagnitudeUnit = driver.configure.gprfMeasurement.iqRecorder.get_munit() \n
		Selects a physical unit for representation of the measured I/Q amplitudes. \n
			:return: magnitude_unit: VOLT | RAW Voltage or raw I/Q data relative to full scale
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MUNit?')
		return Conversions.str_to_scalar_enum(response, enums.MagnitudeUnit)

	def set_munit(self, magnitude_unit: enums.MagnitudeUnit) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MUNit \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.set_munit(magnitude_unit = enums.MagnitudeUnit.RAW) \n
		Selects a physical unit for representation of the measured I/Q amplitudes. \n
			:param magnitude_unit: VOLT | RAW Voltage or raw I/Q data relative to full scale
		"""
		param = Conversions.enum_scalar_to_str(magnitude_unit, enums.MagnitudeUnit)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:MUNit {param}')

	def get_iq_file(self) -> str:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:IQFile \n
		Snippet: value: str = driver.configure.gprfMeasurement.iqRecorder.get_iq_file() \n
		Selects the name and path of the result file. The results are stored in the file in binary format. To write the file,
		start the measurement via INITiate:GPRF:MEAS:IQRecorder ON. \n
			:return: iq_save_file: String parameter to specify the file name and path The supported file name extensions are .iqw and .wv. The extension selects the file type.
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:IQFile?')
		return trim_str_response(response)

	def set_iq_file(self, iq_save_file: str) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:IQFile \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.set_iq_file(iq_save_file = '1') \n
		Selects the name and path of the result file. The results are stored in the file in binary format. To write the file,
		start the measurement via INITiate:GPRF:MEAS:IQRecorder ON. \n
			:param iq_save_file: String parameter to specify the file name and path The supported file name extensions are .iqw and .wv. The extension selects the file type.
		"""
		param = Conversions.value_to_quoted_str(iq_save_file)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:IQFile {param}')

	# noinspection PyTypeChecker
	def get_wt_file(self) -> enums.FileSave:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:WTFile \n
		Snippet: value: enums.FileSave = driver.configure.gprfMeasurement.iqRecorder.get_wt_file() \n
		Selects whether the results are written to an I/Q file, to the memory or both. For file selection, see method RsCma.
		Configure.GprfMeasurement.IqRecorder.iqFile. \n
			:return: save_to_iq_file: OFF | ON | ONLY OFF The results are only stored in the memory. They can be queried via remote control commands. ON The results are stored in the memory and in a file. ONLY The results are only stored in a file. Use this selection if you want to record huge amounts of data that do not fit into the memory.
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:IQRecorder:WTFile?')
		return Conversions.str_to_scalar_enum(response, enums.FileSave)

	def set_wt_file(self, save_to_iq_file: enums.FileSave) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:IQRecorder:WTFile \n
		Snippet: driver.configure.gprfMeasurement.iqRecorder.set_wt_file(save_to_iq_file = enums.FileSave.OFF) \n
		Selects whether the results are written to an I/Q file, to the memory or both. For file selection, see method RsCma.
		Configure.GprfMeasurement.IqRecorder.iqFile. \n
			:param save_to_iq_file: OFF | ON | ONLY OFF The results are only stored in the memory. They can be queried via remote control commands. ON The results are stored in the memory and in a file. ONLY The results are only stored in a file. Use this selection if you want to record huge amounts of data that do not fit into the memory.
		"""
		param = Conversions.enum_scalar_to_str(save_to_iq_file, enums.FileSave)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:IQRecorder:WTFile {param}')

	def clone(self) -> 'IqRecorder':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = IqRecorder(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
