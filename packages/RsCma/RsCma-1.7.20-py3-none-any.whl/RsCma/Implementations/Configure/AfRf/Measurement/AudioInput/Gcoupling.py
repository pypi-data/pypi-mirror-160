from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gcoupling:
	"""Gcoupling commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gcoupling", core, parent)

	def set(self, coupling: enums.GeneratorCoupling, audioInput=repcap.AudioInput.Default) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:GCOupling \n
		Snippet: driver.configure.afRf.measurement.audioInput.gcoupling.set(coupling = enums.GeneratorCoupling.GEN1, audioInput = repcap.AudioInput.Default) \n
		Couples an AF IN connector to an internal signal generator. \n
			:param coupling: OFF | GEN1 | GEN2 | GEN3 | GEN4 OFF No coupling GENn Coupled to audio generator n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
		"""
		param = Conversions.enum_scalar_to_str(coupling, enums.GeneratorCoupling)
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:GCOupling {param}')

	# noinspection PyTypeChecker
	def get(self, audioInput=repcap.AudioInput.Default) -> enums.GeneratorCoupling:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:AIN<nr>:GCOupling \n
		Snippet: value: enums.GeneratorCoupling = driver.configure.afRf.measurement.audioInput.gcoupling.get(audioInput = repcap.AudioInput.Default) \n
		Couples an AF IN connector to an internal signal generator. \n
			:param audioInput: optional repeated capability selector. Default value: Nr1 (settable in the interface 'AudioInput')
			:return: coupling: OFF | GEN1 | GEN2 | GEN3 | GEN4 OFF No coupling GENn Coupled to audio generator n"""
		audioInput_cmd_val = self._cmd_group.get_repcap_cmd_value(audioInput, repcap.AudioInput)
		response = self._core.io.query_str(f'CONFigure:AFRF:MEASurement<Instance>:AIN{audioInput_cmd_val}:GCOupling?')
		return Conversions.str_to_scalar_enum(response, enums.GeneratorCoupling)
