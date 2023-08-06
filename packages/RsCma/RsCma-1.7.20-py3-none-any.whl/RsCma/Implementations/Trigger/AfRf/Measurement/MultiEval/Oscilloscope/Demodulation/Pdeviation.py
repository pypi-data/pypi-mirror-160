from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pdeviation:
	"""Pdeviation commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("pdeviation", core, parent)

	def get_threshold(self) -> float:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:PDEViation:THReshold \n
		Snippet: value: float = driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.pdeviation.get_threshold() \n
		Defines the trigger threshold for the RF input path, for PM demodulation. \n
			:return: threshold: Phase deviation threshold Range: -30 rad to 30 rad, Unit: rad
		"""
		response = self._core.io.query_str('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:PDEViation:THReshold?')
		return Conversions.str_to_float(response)

	def set_threshold(self, threshold: float) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:PDEViation:THReshold \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.demodulation.pdeviation.set_threshold(threshold = 1.0) \n
		Defines the trigger threshold for the RF input path, for PM demodulation. \n
			:param threshold: Phase deviation threshold Range: -30 rad to 30 rad, Unit: rad
		"""
		param = Conversions.decimal_value_to_str(threshold)
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:DEModulation:PDEViation:THReshold {param}')
