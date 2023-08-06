from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserDefined:
	"""UserDefined commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("userDefined", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SCAL:UDEFined:ENABle \n
		Snippet: value: bool = driver.configure.afRf.measurement.multiEval.tones.scal.userDefined.get_enable() \n
		Enables or disables the user-defined tone table. The table is configured via method RsCma.Configure.AfRf.Measurement.
		MultiEval.Tones.Scal.Frequency.value. \n
			:return: user_defined: OFF | ON ON: user-defined tone table OFF: default tone table
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SCAL:UDEFined:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, user_defined: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SCAL:UDEFined:ENABle \n
		Snippet: driver.configure.afRf.measurement.multiEval.tones.scal.userDefined.set_enable(user_defined = False) \n
		Enables or disables the user-defined tone table. The table is configured via method RsCma.Configure.AfRf.Measurement.
		MultiEval.Tones.Scal.Frequency.value. \n
			:param user_defined: OFF | ON ON: user-defined tone table OFF: default tone table
		"""
		param = Conversions.bool_to_str(user_defined)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:MEValuation:TONes:SCAL:UDEFined:ENABle {param}')
