from typing import List

from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dtone:
	"""Dtone commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("dtone", core, parent)

	def set(self, tones_frequency: List[float], frequencyLobe=repcap.FrequencyLobe.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:FREQuency<Nr>:DTONe \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.fdialing.frequency.dtone.set(tones_frequency = [1.1, 2.2, 3.3], frequencyLobe = repcap.FrequencyLobe.Default) \n
		Assigns dual-tone frequencies to digits, for analysis of free-dialing tone sequences. \n
			:param tones_frequency: Comma-separated list of 16 frequencies, assigned to the digits 0, 1, ..., 9, A, ..., F Specifying fewer frequencies leaves the remaining digits unchanged. Range: no=1/2: 60 Hz to 1000 Hz / 1200 Hz to 4000 Hz , Unit: Hz
			:param frequencyLobe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frequency')
		"""
		param = Conversions.list_to_csv_str(tones_frequency)
		frequencyLobe_cmd_val = self._cmd_group.get_repcap_cmd_value(frequencyLobe, repcap.FrequencyLobe)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:FREQuency{frequencyLobe_cmd_val}:DTONe {param}')

	def get(self, frequencyLobe=repcap.FrequencyLobe.Default) -> List[float]:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:FREQuency<Nr>:DTONe \n
		Snippet: value: List[float] = driver.configure.afRf.measurement.multiEval.tones.fdialing.frequency.dtone.get(frequencyLobe = repcap.FrequencyLobe.Default) \n
		Assigns dual-tone frequencies to digits, for analysis of free-dialing tone sequences. \n
			:param frequencyLobe: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Frequency')
			:return: tones_frequency: Comma-separated list of 16 frequencies, assigned to the digits 0, 1, ..., 9, A, ..., F Specifying fewer frequencies leaves the remaining digits unchanged. Range: no=1/2: 60 Hz to 1000 Hz / 1200 Hz to 4000 Hz , Unit: Hz"""
		frequencyLobe_cmd_val = self._cmd_group.get_repcap_cmd_value(frequencyLobe, repcap.FrequencyLobe)
		response = self._core.io.query_bin_or_ascii_float_list(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:FDIaling:FREQuency{frequencyLobe_cmd_val}:DTONe?')
		return response
