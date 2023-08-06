from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal.StructBase import StructBase
from .........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delta:
	"""Delta commands group definition. 2 total commands, 1 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("delta", core, parent)

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_user'):
			from .User import User
			self._user = User(self._core, self._cmd_group)
		return self._user

	# noinspection PyTypeChecker
	class MeasuredStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Left_Meas_Val: float: Unit: Hz
			- Right_Meas_Val: float: Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_float('Left_Meas_Val'),
			ArgStruct.scalar_float('Right_Meas_Val')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Left_Meas_Val: float = None
			self.Right_Meas_Val: float = None

	def get_measured(self) -> MeasuredStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:FMSTereo:FREQuency:DELTa:MEASured \n
		Snippet: value: MeasuredStruct = driver.configure.afRf.measurement.demodulation.fmStereo.frequency.delta.get_measured() \n
		Configures the measured reference value. \n
			:return: structure: for return value, see the help for MeasuredStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:FMSTereo:FREQuency:DELTa:MEASured?', self.__class__.MeasuredStruct())

	def clone(self) -> 'Delta':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Delta(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
