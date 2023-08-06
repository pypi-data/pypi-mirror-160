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
	def get_enable(self) -> enums.DirPwrSensorFwdValue:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:VALue:ENABle \n
		Snippet: value: enums.DirPwrSensorFwdValue = driver.configure.gprfMeasurement.nrt.forward.value.get_enable() \n
		Selects the forward result to be measured. \n
			:return: value: FPWR | PEP | CFAC | CCDF FPWR Forward power PEP Peak envelope power CFAC Crest factor CCDF Complementary cumulative distribution function
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:VALue:ENABle?')
		return Conversions.str_to_scalar_enum(response, enums.DirPwrSensorFwdValue)

	def set_enable(self, value: enums.DirPwrSensorFwdValue) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:VALue:ENABle \n
		Snippet: driver.configure.gprfMeasurement.nrt.forward.value.set_enable(value = enums.DirPwrSensorFwdValue.CCDF) \n
		Selects the forward result to be measured. \n
			:param value: FPWR | PEP | CFAC | CCDF FPWR Forward power PEP Peak envelope power CFAC Crest factor CCDF Complementary cumulative distribution function
		"""
		param = Conversions.enum_scalar_to_str(value, enums.DirPwrSensorFwdValue)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:VALue:ENABle {param}')
