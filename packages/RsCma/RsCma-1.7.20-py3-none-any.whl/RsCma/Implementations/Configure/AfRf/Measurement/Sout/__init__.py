from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sout:
	"""Sout commands group definition. 3 total commands, 2 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sout", core, parent)

	@property
	def enable(self):
		"""enable commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_enable'):
			from .Enable import Enable
			self._enable = Enable(self._core, self._cmd_group)
		return self._enable

	@property
	def level(self):
		"""level commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_level'):
			from .Level import Level
			self._level = Level(self._core, self._cmd_group)
		return self._level

	# noinspection PyTypeChecker
	class SourceStruct(StructBase):  # From ReadStructDefinition CmdPropertyTemplate.xml
		"""Structure for reading output parameters. Fields: \n
			- Source_Left: enums.AudioSource: DEM | DEML Source for the left SPDIF channel DEM Demodulator output (FM, PM, ...) DEML Demodulator output, left channel (FM stereo)
			- Source_Right: enums.AudioSource: DEM | DEMR Source for the right SPDIF channel DEM Demodulator output (FM, PM, ...) DEMR Demodulator output, right channel (FM stereo)"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Source_Left', enums.AudioSource),
			ArgStruct.scalar_enum('Source_Right', enums.AudioSource)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Source_Left: enums.AudioSource = None
			self.Source_Right: enums.AudioSource = None

	def get_source(self) -> SourceStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SOUT:SOURce \n
		Snippet: value: SourceStruct = driver.configure.afRf.measurement.sout.get_source() \n
		Sets the audio signal sources for the SPDIF OUT connector. \n
			:return: structure: for return value, see the help for SourceStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SOUT:SOURce?', self.__class__.SourceStruct())

	def clone(self) -> 'Sout':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sout(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
