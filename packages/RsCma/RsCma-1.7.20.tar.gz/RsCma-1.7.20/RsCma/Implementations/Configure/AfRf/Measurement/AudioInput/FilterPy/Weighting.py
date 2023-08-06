from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Weighting:
	"""Weighting commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("weighting", core, parent)

	def set(self, filter_py: enums.WeightingFilter, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:WEIGhting \n
		Snippet: driver.configure.afRf.measurement.audioInput.filterPy.weighting.set(filter_py = enums.WeightingFilter.AWEighting, audioInput = repcap.AudioInput.Default) \n
		Configures the weighting filter in an AF input path. \n
			:param filter_py: OFF | AWEighting | CCITt | CMESsage OFF Filter disabled AWEighting A-weighting filter CCITt CCITT weighting filter CMESsage C-message weighting filter
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(filter_py, enums.WeightingFilter)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:WEIGhting {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.WeightingFilter:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:FILTer:WEIGhting \n
		Snippet: value: enums.WeightingFilter = driver.configure.afRf.measurement.audioInput.filterPy.weighting.get(audioInput = repcap.AudioInput.Default) \n
		Configures the weighting filter in an AF input path. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: filter_py: OFF | AWEighting | CCITt | CMESsage OFF Filter disabled AWEighting A-weighting filter CCITt CCITT weighting filter CMESsage C-message weighting filter"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:FILTer:WEIGhting?')
		return Conversions.str_to_scalar_enum(response, enums.WeightingFilter)
