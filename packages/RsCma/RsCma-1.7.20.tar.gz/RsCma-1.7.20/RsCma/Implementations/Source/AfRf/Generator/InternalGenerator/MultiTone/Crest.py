from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Crest:
	"""Crest commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("crest", core, parent)

	def set(self, crest_factor: enums.CrestFactor, internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:CRESt \n
		Snippet: driver.source.afRf.generator.internalGenerator.multiTone.crest.set(crest_factor = enums.CrestFactor.LOW, internalGen = repcap.InternalGen.Default) \n
		Configures the crest factor for multitone signal generation. \n
			:param crest_factor: MAXimum | LOW
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
		"""
		param = Conversions.enum_scalar_to_str(crest_factor, enums.CrestFactor)
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:CRESt {param}')

	# noinspection PyTypeChecker
	def get(self, internalGen=repcap.InternalGen.Default) -> enums.CrestFactor:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:CRESt \n
		Snippet: value: enums.CrestFactor = driver.source.afRf.generator.internalGenerator.multiTone.crest.get(internalGen = repcap.InternalGen.Default) \n
		Configures the crest factor for multitone signal generation. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: crest_factor: MAXimum | LOW"""
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:CRESt?')
		return Conversions.str_to_scalar_enum(response, enums.CrestFactor)
