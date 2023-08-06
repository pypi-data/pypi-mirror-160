from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Level:
	"""Level commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("level", core, parent)

	def set(self, level_edit_mode: enums.LevelEditMode, internalGen=repcap.InternalGen.Default) -> None:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:LEVel \n
		Snippet: driver.source.afRf.generator.internalGenerator.multiTone.level.set(level_edit_mode = enums.LevelEditMode.INDividual, internalGen = repcap.InternalGen.Default) \n
		Selects an edit mode for multitone level configuration. \n
			:param level_edit_mode: TOTal | INDividual TOTal All tones have the same level. To configure the total level, see: method RsCma.Source.AfRf.Generator.InternalGenerator.MultiTone.Tlevel.set INDividual The level of each tone is configured separately, see: method RsCma.Source.AfRf.Generator.InternalGenerator.MultiTone.Ilevel.set
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
		"""
		param = Conversions.enum_scalar_to_str(level_edit_mode, enums.LevelEditMode)
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		self._core.io.write(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:LEVel {param}')

	# noinspection PyTypeChecker
	def get(self, internalGen=repcap.InternalGen.Default) -> enums.LevelEditMode:
		"""SCPI: SOURce:AFRF:GENerator<Instance>:IGENerator<nr>:MTONe:LEVel \n
		Snippet: value: enums.LevelEditMode = driver.source.afRf.generator.internalGenerator.multiTone.level.get(internalGen = repcap.InternalGen.Default) \n
		Selects an edit mode for multitone level configuration. \n
			:param internalGen: optional repeated capability selector. Default value: Nr1 (settable in the interface 'InternalGenerator')
			:return: level_edit_mode: TOTal | INDividual TOTal All tones have the same level. To configure the total level, see: method RsCma.Source.AfRf.Generator.InternalGenerator.MultiTone.Tlevel.set INDividual The level of each tone is configured separately, see: method RsCma.Source.AfRf.Generator.InternalGenerator.MultiTone.Ilevel.set"""
		internalGen_cmd_val = self._cmd_group.get_repcap_cmd_value(internalGen, repcap.InternalGen)
		response = self._core.io.query_str(f'SOURce:AFRF:GENerator<Instance>:IGENerator{internalGen_cmd_val}:MTONe:LEVel?')
		return Conversions.str_to_scalar_enum(response, enums.LevelEditMode)
