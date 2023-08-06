from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Arb:
	"""Arb commands group definition. 6 total commands, 2 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("arb", core, parent)

	@property
	def catalog(self):
		"""catalog commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import Catalog
			self._catalog = Catalog(self._core, self._cmd_group)
		return self._catalog

	@property
	def manual(self):
		"""manual commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_manual'):
			from .Manual import Manual
			self._manual = Manual(self._core, self._cmd_group)
		return self._manual

	def get_autostart(self) -> bool:
		"""SCPI: TRIGger:AFRF:GENerator<Instance>:ARB:AUTostart \n
		Snippet: value: bool = driver.trigger.afRf.generator.arb.get_autostart() \n
		Enables or disables the automatic start of the loaded ARB file whenever the generator is turned on. This setting applies
		only to the 'Manual' trigger source. For other trigger sources, autostart is disabled. \n
			:return: autostart: OFF | ON
		"""
		response = self._core.io.query_str('TRIGger:AFRF:GENerator<Instance>:ARB:AUTostart?')
		return Conversions.str_to_bool(response)

	def set_autostart(self, autostart: bool) -> None:
		"""SCPI: TRIGger:AFRF:GENerator<Instance>:ARB:AUTostart \n
		Snippet: driver.trigger.afRf.generator.arb.set_autostart(autostart = False) \n
		Enables or disables the automatic start of the loaded ARB file whenever the generator is turned on. This setting applies
		only to the 'Manual' trigger source. For other trigger sources, autostart is disabled. \n
			:param autostart: OFF | ON
		"""
		param = Conversions.bool_to_str(autostart)
		self._core.io.write(f'TRIGger:AFRF:GENerator<Instance>:ARB:AUTostart {param}')

	def get_delay(self) -> float:
		"""SCPI: TRIGger:AFRF:GENerator<Instance>:ARB:DELay \n
		Snippet: value: float = driver.trigger.afRf.generator.arb.get_delay() \n
		Specifies a start delay relative to the trigger event. This setting is ignored for the 'Manual' trigger source. \n
			:return: delay: Range: 0 s to 100 s, Unit: s
		"""
		response = self._core.io.query_str('TRIGger:AFRF:GENerator<Instance>:ARB:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""SCPI: TRIGger:AFRF:GENerator<Instance>:ARB:DELay \n
		Snippet: driver.trigger.afRf.generator.arb.set_delay(delay = 1.0) \n
		Specifies a start delay relative to the trigger event. This setting is ignored for the 'Manual' trigger source. \n
			:param delay: Range: 0 s to 100 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'TRIGger:AFRF:GENerator<Instance>:ARB:DELay {param}')

	def get_retrigger(self) -> bool:
		"""SCPI: TRIGger:AFRF:GENerator<Instance>:ARB:RETRigger \n
		Snippet: value: bool = driver.trigger.afRf.generator.arb.get_retrigger() \n
		Specifies whether trigger events during ARB file processing restart the ARB file or not. This setting applies only to the
		'Manual' trigger source. For other trigger sources, retriggering is disabled. \n
			:return: retrigger: OFF | ON
		"""
		response = self._core.io.query_str('TRIGger:AFRF:GENerator<Instance>:ARB:RETRigger?')
		return Conversions.str_to_bool(response)

	def set_retrigger(self, retrigger: bool) -> None:
		"""SCPI: TRIGger:AFRF:GENerator<Instance>:ARB:RETRigger \n
		Snippet: driver.trigger.afRf.generator.arb.set_retrigger(retrigger = False) \n
		Specifies whether trigger events during ARB file processing restart the ARB file or not. This setting applies only to the
		'Manual' trigger source. For other trigger sources, retriggering is disabled. \n
			:param retrigger: OFF | ON
		"""
		param = Conversions.bool_to_str(retrigger)
		self._core.io.write(f'TRIGger:AFRF:GENerator<Instance>:ARB:RETRigger {param}')

	def get_source(self) -> str:
		"""SCPI: TRIGger:AFRF:GENerator<Instance>:ARB:SOURce \n
		Snippet: value: str = driver.trigger.afRf.generator.arb.get_source() \n
		Selects the trigger event source used to start or restart ARB file processing. To query a list of all supported sources,
		use method RsCma.Trigger.AfRf.Generator.Arb.Catalog.source. \n
			:return: source: 'Manual' Manual start via method RsCma.Trigger.AfRf.Generator.Arb.Manual.Execute.set 'Base1: External TRIG In' External trigger signal received at connector TRIG IN
		"""
		response = self._core.io.query_str('TRIGger:AFRF:GENerator<Instance>:ARB:SOURce?')
		return trim_str_response(response)

	def set_source(self, source: str) -> None:
		"""SCPI: TRIGger:AFRF:GENerator<Instance>:ARB:SOURce \n
		Snippet: driver.trigger.afRf.generator.arb.set_source(source = '1') \n
		Selects the trigger event source used to start or restart ARB file processing. To query a list of all supported sources,
		use method RsCma.Trigger.AfRf.Generator.Arb.Catalog.source. \n
			:param source: 'Manual' Manual start via method RsCma.Trigger.AfRf.Generator.Arb.Manual.Execute.set 'Base1: External TRIG In' External trigger signal received at connector TRIG IN
		"""
		param = Conversions.value_to_quoted_str(source)
		self._core.io.write(f'TRIGger:AFRF:GENerator<Instance>:ARB:SOURce {param}')

	def clone(self) -> 'Arb':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Arb(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
