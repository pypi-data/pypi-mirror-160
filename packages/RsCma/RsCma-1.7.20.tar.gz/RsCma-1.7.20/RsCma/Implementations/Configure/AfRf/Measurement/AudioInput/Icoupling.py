from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Icoupling:
	"""Icoupling commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("icoupling", core, parent)

	def set(self, path_coupling: enums.PathCoupling, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:ICOupling \n
		Snippet: driver.configure.afRf.measurement.audioInput.icoupling.set(path_coupling = enums.PathCoupling.AC, audioInput = repcap.AudioInput.Default) \n
		Configures whether the DC signal component is blocked at an AF IN connector, or not. \n
			:param path_coupling: AC | DC AC DC component blocked, only AC component available DC AC and DC component available
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(path_coupling, enums.PathCoupling)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:ICOupling {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.PathCoupling:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:ICOupling \n
		Snippet: value: enums.PathCoupling = driver.configure.afRf.measurement.audioInput.icoupling.get(audioInput = repcap.AudioInput.Default) \n
		Configures whether the DC signal component is blocked at an AF IN connector, or not. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: path_coupling: AC | DC AC DC component blocked, only AC component available DC AC and DC component available"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:ICOupling?')
		return Conversions.str_to_scalar_enum(response, enums.PathCoupling)
