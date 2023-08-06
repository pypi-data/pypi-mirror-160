from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Marker:
	"""Marker commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("marker", core, parent)

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import Enable
			self._enable = Enable(self._core, self._cmd_group)
		return self._enable

	# noinspection PyTypeChecker
	def get_detector(self) -> enums.Detector:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:MARKer:DETector \n
		Snippet: value: enums.Detector = driver.configure.gprfMeasurement.spectrum.marker.get_detector() \n
		Selects the detector used to calculate the 1001 values of the result traces from the raw set of samples. \n
			:return: detector: AVERage | RMS | SAMPle | MINPeak | MAXPeak | AUTopeak
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:MARKer:DETector?')
		return Conversions.str_to_scalar_enum(response, enums.Detector)

	def set_detector(self, detector: enums.Detector) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:MARKer:DETector \n
		Snippet: driver.configure.gprfMeasurement.spectrum.marker.set_detector(detector = enums.Detector.AUTopeak) \n
		Selects the detector used to calculate the 1001 values of the result traces from the raw set of samples. \n
			:param detector: AVERage | RMS | SAMPle | MINPeak | MAXPeak | AUTopeak
		"""
		param = Conversions.enum_scalar_to_str(detector, enums.Detector)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:MARKer:DETector {param}')

	def clone(self) -> 'Marker':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Marker(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
