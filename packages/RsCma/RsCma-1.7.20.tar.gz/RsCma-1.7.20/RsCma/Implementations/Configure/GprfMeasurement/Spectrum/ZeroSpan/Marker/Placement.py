from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Placement:
	"""Placement commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("placement", core, parent)

	def set(self, placement: enums.MarkerPlacement, markerOther=repcap.MarkerOther.Nr2) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer<nr>:PLACement \n
		Snippet: driver.configure.gprfMeasurement.spectrum.zeroSpan.marker.placement.set(placement = enums.MarkerPlacement.ABSolute, markerOther = repcap.MarkerOther.Nr2) \n
		Selects between absolute coordinates and coordinates relative to the reference marker, for marker number <no> and zero
		span mode. \n
			:param placement: ABSolute | RELative
			:param markerOther: optional repeated capability selector. Default value: Nr2
		"""
		param = Conversions.enum_scalar_to_str(placement, enums.MarkerPlacement)
		markerOther_cmd_val = self._cmd_group.get_repcap_cmd_value(markerOther, repcap.MarkerOther)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer{markerOther_cmd_val}:PLACement {param}')

	# noinspection PyTypeChecker
	def get(self, markerOther=repcap.MarkerOther.Nr2) -> enums.MarkerPlacement:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer<nr>:PLACement \n
		Snippet: value: enums.MarkerPlacement = driver.configure.gprfMeasurement.spectrum.zeroSpan.marker.placement.get(markerOther = repcap.MarkerOther.Nr2) \n
		Selects between absolute coordinates and coordinates relative to the reference marker, for marker number <no> and zero
		span mode. \n
			:param markerOther: optional repeated capability selector. Default value: Nr2
			:return: placement: ABSolute | RELative"""
		markerOther_cmd_val = self._cmd_group.get_repcap_cmd_value(markerOther, repcap.MarkerOther)
		response = self._core.io.query_str(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:MARKer{markerOther_cmd_val}:PLACement?')
		return Conversions.str_to_scalar_enum(response, enums.MarkerPlacement)
