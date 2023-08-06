from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delta:
	"""Delta commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delta", core, parent)

	def get_user(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN:SECond:LEVel:DELTa:USER \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.second.level.delta.get_user() \n
		Configures the AF2 level reference mode. \n
			:return: user_val: Unit: V
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:AIN:SECond:LEVel:DELTa:USER?')
		return Conversions.str_to_float(response)

	def set_user(self, user_val: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN:SECond:LEVel:DELTa:USER \n
		Snippet: driver.configure.afRf.measurement.audioInput.second.level.delta.set_user(user_val = 1.0) \n
		Configures the AF2 level reference mode. \n
			:param user_val: Unit: V
		"""
		param = Conversions.decimal_value_to_str(user_val)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN:SECond:LEVel:DELTa:USER {param}')

	def get_measured(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN:SECond:LEVel:DELTa:MEASured \n
		Snippet: value: float = driver.configure.afRf.measurement.audioInput.second.level.delta.get_measured() \n
		Configures the AF2 level measured reference value. \n
			:return: meas_val: Unit: V
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:AIN:SECond:LEVel:DELTa:MEASured?')
		return Conversions.str_to_float(response)
