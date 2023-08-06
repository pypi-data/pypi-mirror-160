from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Value:
	"""Value commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("value", core, parent)

	# noinspection PyTypeChecker
	def get_enable(self) -> enums.DirPwrSensorRevValue:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:VALue:ENABle \n
		Snippet: value: enums.DirPwrSensorRevValue = driver.configure.gprfMeasurement.nrt.reverse.value.get_enable() \n
		Selects the reverse result to be measured.
			INTRO_CMD_HELP: The effect of the value RPWR depends on the value set via the command method RsCma.Configure.GprfMeasurement.Nrt.Forward.Value.enable: \n
			- FPWR or PEP: RPWR selects the reverse power result
			- CFAC or CCDF: RPWR selects the forward power result \n
			:return: value: RPWR | RLOS | REFL | SWR RPWR Reverse power or forward power RLOS Return loss REFL Reflection SWR Standing wave ratio
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:VALue:ENABle?')
		return Conversions.str_to_scalar_enum(response, enums.DirPwrSensorRevValue)

	def set_enable(self, value: enums.DirPwrSensorRevValue) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:VALue:ENABle \n
		Snippet: driver.configure.gprfMeasurement.nrt.reverse.value.set_enable(value = enums.DirPwrSensorRevValue.REFL) \n
		Selects the reverse result to be measured.
			INTRO_CMD_HELP: The effect of the value RPWR depends on the value set via the command method RsCma.Configure.GprfMeasurement.Nrt.Forward.Value.enable: \n
			- FPWR or PEP: RPWR selects the reverse power result
			- CFAC or CCDF: RPWR selects the forward power result \n
			:param value: RPWR | RLOS | REFL | SWR RPWR Reverse power or forward power RLOS Return loss REFL Reflection SWR Standing wave ratio
		"""
		param = Conversions.enum_scalar_to_str(value, enums.DirPwrSensorRevValue)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:VALue:ENABle {param}')
