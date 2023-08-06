from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Frequency:
	"""Frequency commands group definition. 6 total commands, 1 Subgroups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("frequency", core, parent)

	@property
	def delta(self):
		"""delta commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_delta'):
			from .Delta import Delta
			self._delta = Delta(self._core, self._cmd_group)
		return self._delta

	def get_atg_frequency(self) -> bool:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FREQuency:ATGFrequency \n
		Snippet: value: bool = driver.configure.afRf.measurement.voip.frequency.get_atg_frequency() \n
		Selects whether the carrier center frequency resulting from the FID is copied from the analyzer to the AFRF generator or
		not. \n
			:return: apply_to_gen_rf: OFF | ON
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:VOIP:FREQuency:ATGFrequency?')
		return Conversions.str_to_bool(response)

	def set_atg_frequency(self, apply_to_gen_rf: bool) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FREQuency:ATGFrequency \n
		Snippet: driver.configure.afRf.measurement.voip.frequency.set_atg_frequency(apply_to_gen_rf = False) \n
		Selects whether the carrier center frequency resulting from the FID is copied from the analyzer to the AFRF generator or
		not. \n
			:param apply_to_gen_rf: OFF | ON
		"""
		param = Conversions.bool_to_str(apply_to_gen_rf)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:VOIP:FREQuency:ATGFrequency {param}')

	# noinspection PyTypeChecker
	class ValueStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Frequency: float: RF carrier center frequency Unit: Hz
			- Channel_Spacing: float: Channel spacing Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Frequency'),
			ArgStruct.scalar_float('Channel_Spacing')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Frequency: float = None
			self.Channel_Spacing: float = None

	def get_value(self) -> ValueStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:VOIP:FREQuency \n
		Snippet: value: ValueStruct = driver.configure.afRf.measurement.voip.frequency.get_value() \n
		Queries the RF carrier center frequency and the channel spacing resulting from the configured frequency ID. \n
			:return: structure: for return value, see the help for ValueStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:VOIP:FREQuency?', self.__class__.ValueStruct())

	def clone(self) -> 'Frequency':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Frequency(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
