from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tmode:
	"""Tmode commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("tmode", core, parent)

	def set(self, tone_type: enums.ToneTypeA, internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:TMODe \n
		Snippet: driver.source.afRf.generator.internalGenerator.tmode.set(tone_type = enums.ToneTypeA.DTMF, internalGen = repcap.InternalGen.Default) \n
		Selects the tone mode of an internal audio generator. \n
			:param tone_type: STONe | DTONe | MTONe | NOISe | DTMF | SELCall | FDIaling | SCAL | SQUare STONe Single-tone signal DTONe Dual-tone signal MTONe Multitone signal NOISe Noise signal DTMF DTMF sequence SELCall SelCall selective calling FDIaling Free dialing SCAL SELCAL selective calling SQUare Square signal
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
		"""
		param = Conversions.enum_scalar_to_str(tone_type, enums.ToneTypeA)
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:TMODe {param}')

	# noinspection PyTypeChecker
	def get(self, internalGen=repcap.InternalGen.Default) -> enums.ToneTypeA:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:TMODe \n
		Snippet: value: enums.ToneTypeA = driver.source.afRf.generator.internalGenerator.tmode.get(internalGen = repcap.InternalGen.Default) \n
		Selects the tone mode of an internal audio generator. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: tone_type: STONe | DTONe | MTONe | NOISe | DTMF | SELCall | FDIaling | SCAL | SQUare STONe Single-tone signal DTONe Dual-tone signal MTONe Multitone signal NOISe Noise signal DTMF DTMF sequence SELCall SelCall selective calling FDIaling Free dialing SCAL SELCAL selective calling SQUare Square signal"""
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.ToneTypeA)
