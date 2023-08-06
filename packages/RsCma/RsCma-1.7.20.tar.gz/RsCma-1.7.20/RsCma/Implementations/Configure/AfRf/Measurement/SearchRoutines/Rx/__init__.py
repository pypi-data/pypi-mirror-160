from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rx:
	"""Rx commands group definition. 3 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rx", core, parent)

	@property
	def amPoints(self):
		"""amPoints commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_amPoints'):
			from .AmPoints import AmPoints
			self._amPoints = AmPoints(self._core, self._cmd_group)
		return self._amPoints

	def get_se_time(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RX:SETime \n
		Snippet: value: float = driver.configure.afRf.measurement.searchRoutines.rx.get_se_time() \n
		Waiting time after a change of the signal properties before the measurement is started. \n
			:return: setting_time: Unit: s
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:RX:SETime?')
		return Conversions.str_to_float(response)

	def set_se_time(self, setting_time: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RX:SETime \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.rx.set_se_time(setting_time = 1.0) \n
		Waiting time after a change of the signal properties before the measurement is started. \n
			:param setting_time: Unit: s
		"""
		param = Conversions.decimal_value_to_str(setting_time)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:RX:SETime {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.SearchRoutine:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RX:MODE \n
		Snippet: value: enums.SearchRoutine = driver.configure.afRf.measurement.searchRoutines.rx.get_mode() \n
		Selects the RX search routine to be performed. \n
			:return: search_routine: RSENsitivity | RSQuelch | RIFBandwidth | SSNR RSENsitivity 'RX Sensitivity' RSQuelch 'RX Squelch' RIFBandwidth 'RX Bandwidth' SSNR 'Switched SNR'
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:RX:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.SearchRoutine)

	def set_mode(self, search_routine: enums.SearchRoutine) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RX:MODE \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.rx.set_mode(search_routine = enums.SearchRoutine.ADELay) \n
		Selects the RX search routine to be performed. \n
			:param search_routine: RSENsitivity | RSQuelch | RIFBandwidth | SSNR RSENsitivity 'RX Sensitivity' RSQuelch 'RX Squelch' RIFBandwidth 'RX Bandwidth' SSNR 'Switched SNR'
		"""
		param = Conversions.enum_scalar_to_str(search_routine, enums.SearchRoutine)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:RX:MODE {param}')

	def clone(self) -> 'Rx':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rx(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
