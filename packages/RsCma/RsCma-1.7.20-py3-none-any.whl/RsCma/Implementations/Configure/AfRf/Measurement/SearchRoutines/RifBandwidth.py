from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RifBandwidth:
	"""RifBandwidth commands group definition. 2 total commands, 0 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rifBandwidth", core, parent)

	def get_sd_method(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:SDMethod \n
		Snippet: value: bool = driver.configure.afRf.measurement.searchRoutines.rifBandwidth.get_sd_method() \n
		If enabled, the search routine follows the TIA-603-D specification determining the signal displacement bandwidth and
		starting from the RX sensitivity level. If disabled, the search routine uses a noise level method determining the
		bandwidth, not relying on the RX sensitivity. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:SDMethod?')
		return Conversions.str_to_bool(response)

	def set_sd_method(self, enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:SDMethod \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.rifBandwidth.set_sd_method(enable = False) \n
		If enabled, the search routine follows the TIA-603-D specification determining the signal displacement bandwidth and
		starting from the RX sensitivity level. If disabled, the search routine uses a noise level method determining the
		bandwidth, not relying on the RX sensitivity. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:SDMethod {param}')

	def get_rs_results(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:RSResults \n
		Snippet: value: bool = driver.configure.afRf.measurement.searchRoutines.rifBandwidth.get_rs_results() \n
		If enabled, the result of a previously run RX sensitivity search routine is used. If disabled, the RX sensitivity is
		determined at the first phase of the search routine. \n
			:return: enable: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:RSResults?')
		return Conversions.str_to_bool(response)

	def set_rs_results(self, enable: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:RSResults \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.rifBandwidth.set_rs_results(enable = False) \n
		If enabled, the result of a previously run RX sensitivity search routine is used. If disabled, the RX sensitivity is
		determined at the first phase of the search routine. \n
			:param enable: OFF | ON
		"""
		param = Conversions.bool_to_str(enable)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:RIFBandwidth:RSResults {param}')
