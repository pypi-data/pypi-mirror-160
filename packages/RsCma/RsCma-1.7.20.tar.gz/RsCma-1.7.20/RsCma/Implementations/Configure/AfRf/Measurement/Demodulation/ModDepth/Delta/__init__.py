from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delta:
	"""Delta commands group definition. 4 total commands, 1 Subgroups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delta", core, parent)

	@property
	def update(self):
		"""update commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_update'):
			from .Update import Update
			self._update = Update(self._core, self._cmd_group)
		return self._update

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.DeltaMode:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:MDEPth:DELTa:MODE \n
		Snippet: value: enums.DeltaMode = driver.configure.afRf.measurement.demodulation.modDepth.delta.get_mode() \n
		Sets the mode for the reference value of the modulation depth for AM demodulation. \n
			:return: mode: NONE | MEAS | USER NONE No reference value, delta measurement is disabled MEAS Measured reference value USER User-defined reference value
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation:MDEPth:DELTa:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DeltaMode)

	def set_mode(self, mode: enums.DeltaMode) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:MDEPth:DELTa:MODE \n
		Snippet: driver.configure.afRf.measurement.demodulation.modDepth.delta.set_mode(mode = enums.DeltaMode.MEAS) \n
		Sets the mode for the reference value of the modulation depth for AM demodulation. \n
			:param mode: NONE | MEAS | USER NONE No reference value, delta measurement is disabled MEAS Measured reference value USER User-defined reference value
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.DeltaMode)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:MDEPth:DELTa:MODE {param}')

	def get_user(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:MDEPth:DELTa:USER \n
		Snippet: value: float = driver.configure.afRf.measurement.demodulation.modDepth.delta.get_user() \n
		Configures the user-defined reference value of the modulation depth for AM demodulation. \n
			:return: user_val: Range: 0.01 % to 100.00 % , Unit: %
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation:MDEPth:DELTa:USER?')
		return Conversions.str_to_float(response)

	def set_user(self, user_val: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:MDEPth:DELTa:USER \n
		Snippet: driver.configure.afRf.measurement.demodulation.modDepth.delta.set_user(user_val = 1.0) \n
		Configures the user-defined reference value of the modulation depth for AM demodulation. \n
			:param user_val: Range: 0.01 % to 100.00 % , Unit: %
		"""
		param = Conversions.decimal_value_to_str(user_val)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:MDEPth:DELTa:USER {param}')

	def get_measured(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:MDEPth:DELTa:MEASured \n
		Snippet: value: float = driver.configure.afRf.measurement.demodulation.modDepth.delta.get_measured() \n
		Configures the measured reference value of the modulation depth for AM demodulation. \n
			:return: meas_val: Range: 0.01 % to 100.00 % , Unit: %
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation:MDEPth:DELTa:MEASured?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Delta':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Delta(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
