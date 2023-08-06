from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class First:
	"""First commands group definition. 3 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("first", core, parent)

	@property
	def level(self):
		"""level commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Level import Level
			self._level = Level(self._core, self._cmd_group)
		return self._level

	def get_mlevel(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN:FIRSt:MLEVel \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.first.get_mlevel() \n
		Specifies the maximum expected level for the AF1 IN connector. This setting is only relevant, if auto ranging is disabled.
		Use this command, if you want to set different level units, e.g. dBm (Table 'Units relevant for remote commands') , or
		set the level for both connectors independently. \n
			:return: max_level: Range: 10E-6 V to 43 V, Unit: V
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:AIN:FIRSt:MLEVel?')
		return Conversions.str_to_float(response)

	def set_mlevel(self, max_level: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN:FIRSt:MLEVel \n
		Snippet: driver.configure.afRf.measurement.audioInput.first.set_mlevel(max_level = 1.0) \n
		Specifies the maximum expected level for the AF1 IN connector. This setting is only relevant, if auto ranging is disabled.
		Use this command, if you want to set different level units, e.g. dBm (Table 'Units relevant for remote commands') , or
		set the level for both connectors independently. \n
			:param max_level: Range: 10E-6 V to 43 V, Unit: V
		"""
		param = Conversions.decimal_value_to_str(max_level)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN:FIRSt:MLEVel {param}')

	def clone(self) -> 'First':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = First(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
