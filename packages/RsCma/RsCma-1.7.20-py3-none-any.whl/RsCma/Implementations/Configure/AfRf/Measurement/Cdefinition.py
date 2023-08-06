from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cdefinition:
	"""Cdefinition commands group definition. 4 total commands, 0 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("cdefinition", core, parent)

	def get_rchannel(self) -> int:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:CDEFinition:RCHannel \n
		Snippet: value: int = driver.configure.afRf.measurement.cdefinition.get_rchannel() \n
		Assigns a reference channel number to the reference frequency defined via method RsCma.Configure.AfRf.Measurement.
		Cdefinition.rfrequency. This setting is part of the channel definition. \n
			:return: reference_ch: Range: 0 Ch to 9999 Ch, Unit: Ch
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:CDEFinition:RCHannel?')
		return Conversions.str_to_int(response)

	def set_rchannel(self, reference_ch: int) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:CDEFinition:RCHannel \n
		Snippet: driver.configure.afRf.measurement.cdefinition.set_rchannel(reference_ch = 1) \n
		Assigns a reference channel number to the reference frequency defined via method RsCma.Configure.AfRf.Measurement.
		Cdefinition.rfrequency. This setting is part of the channel definition. \n
			:param reference_ch: Range: 0 Ch to 9999 Ch, Unit: Ch
		"""
		param = Conversions.decimal_value_to_str(reference_ch)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:CDEFinition:RCHannel {param}')

	def get_rfrequency(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:CDEFinition:RFRequency \n
		Snippet: value: float = driver.configure.afRf.measurement.cdefinition.get_rfrequency() \n
		Assigns a reference frequency to the reference channel number defined via method RsCma.Configure.AfRf.Measurement.
		Cdefinition.rchannel. This setting is part of the channel definition. \n
			:return: reference_freq: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:CDEFinition:RFRequency?')
		return Conversions.str_to_float(response)

	def set_rfrequency(self, reference_freq: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:CDEFinition:RFRequency \n
		Snippet: driver.configure.afRf.measurement.cdefinition.set_rfrequency(reference_freq = 1.0) \n
		Assigns a reference frequency to the reference channel number defined via method RsCma.Configure.AfRf.Measurement.
		Cdefinition.rchannel. This setting is part of the channel definition. \n
			:param reference_freq: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(reference_freq)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:CDEFinition:RFRequency {param}')

	def get_cspace(self) -> float:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:CDEFinition:CSPace \n
		Snippet: value: float = driver.configure.afRf.measurement.cdefinition.get_cspace() \n
		Defines the channel spacing, that is the center frequency difference of two adjacent channels. This setting is part of
		the channel definition. \n
			:return: channel_space: Range: 100 Hz to 4 MHz, Unit: Hz
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:CDEFinition:CSPace?')
		return Conversions.str_to_float(response)

	def set_cspace(self, channel_space: float) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:CDEFinition:CSPace \n
		Snippet: driver.configure.afRf.measurement.cdefinition.set_cspace(channel_space = 1.0) \n
		Defines the channel spacing, that is the center frequency difference of two adjacent channels. This setting is part of
		the channel definition. \n
			:param channel_space: Range: 100 Hz to 4 MHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(channel_space)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:CDEFinition:CSPace {param}')

	def get_value(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:CDEFinition \n
		Snippet: value: bool = driver.configure.afRf.measurement.cdefinition.get_value() \n
		Activates or deactivates the channel definition. \n
			:return: reference_ch: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:CDEFinition?')
		return Conversions.str_to_bool(response)

	def set_value(self, reference_ch: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:CDEFinition \n
		Snippet: driver.configure.afRf.measurement.cdefinition.set_value(reference_ch = False) \n
		Activates or deactivates the channel definition. \n
			:param reference_ch: OFF | ON
		"""
		param = Conversions.bool_to_str(reference_ch)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:CDEFinition {param}')
