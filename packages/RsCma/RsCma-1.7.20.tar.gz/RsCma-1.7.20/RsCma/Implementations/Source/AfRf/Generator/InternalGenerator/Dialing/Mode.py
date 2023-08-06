from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mode:
	"""Mode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("mode", core, parent)

	def set(self, tone_type: enums.DialingMode, internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:DIALing:MODE \n
		Snippet: driver.source.afRf.generator.internalGenerator.dialing.mode.set(tone_type = enums.DialingMode.DTMF, internalGen = repcap.InternalGen.Default) \n
		Selects the dialing mode of an internal audio generator. This command is only relevant for non-dialing tone modes, for
		example tone mode 'single tone' plus dialing mode 'DTMF'. \n
			:param tone_type: DTMF | SELCall | FDIaling | SCAL DTMF DTMF sequence SELCall SelCall selective calling FDIaling Free dialing SCAL SELCAL selective calling
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
		"""
		param = Conversions.enum_scalar_to_str(tone_type, enums.DialingMode)
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:DIALing:MODE {param}')

	# noinspection PyTypeChecker
	def get(self, internalGen=repcap.InternalGen.Default) -> enums.DialingMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:DIALing:MODE \n
		Snippet: value: enums.DialingMode = driver.source.afRf.generator.internalGenerator.dialing.mode.get(internalGen = repcap.InternalGen.Default) \n
		Selects the dialing mode of an internal audio generator. This command is only relevant for non-dialing tone modes, for
		example tone mode 'single tone' plus dialing mode 'DTMF'. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: tone_type: DTMF | SELCall | FDIaling | SCAL DTMF DTMF sequence SELCall SelCall selective calling FDIaling Free dialing SCAL SELCAL selective calling"""
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:DIALing:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.DialingMode)
