from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class UserDefined:
	"""UserDefined commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("userDefined", core, parent)

	def get_enable(self) -> bool:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:UDEFined:ENABle \n
		Snippet: value: bool = driver.source.afRf.generator.dialing.dtmf.userDefined.get_enable() \n
		Enables or disables the user-defined tone table. The table is configured via method RsCma.Source.AfRf.Generator.Dialing.
		Dtmf.Frequency.value. \n
			:return: dtmf_userdefined: OFF | ON ON: user-defined tone table OFF: default tone table
		"""
		response = self._core.io.query_str('SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:UDEFined:ENABle?')
		return Conversions.str_to_bool(response)

	def set_enable(self, dtmf_userdefined: bool) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:UDEFined:ENABle \n
		Snippet: driver.source.afRf.generator.dialing.dtmf.userDefined.set_enable(dtmf_userdefined = False) \n
		Enables or disables the user-defined tone table. The table is configured via method RsCma.Source.AfRf.Generator.Dialing.
		Dtmf.Frequency.value. \n
			:param dtmf_userdefined: OFF | ON ON: user-defined tone table OFF: default tone table
		"""
		param = Conversions.bool_to_str(dtmf_userdefined)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:DIALing:DTMF:UDEFined:ENABle {param}')
