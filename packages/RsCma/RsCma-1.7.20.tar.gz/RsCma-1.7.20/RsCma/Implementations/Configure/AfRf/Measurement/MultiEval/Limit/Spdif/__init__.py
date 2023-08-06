from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spdif:
	"""Spdif commands group definition. 6 total commands, 2 Subgroups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("spdif", core, parent)

	@property
	def thDistortion(self):
		"""thDistortion commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_thDistortion'):
			from .ThDistortion import ThDistortion
			self._thDistortion = ThDistortion(self._core, self._cmd_group)
		return self._thDistortion

	@property
	def thdNoise(self):
		"""thdNoise commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_thdNoise'):
			from .ThdNoise import ThdNoise
			self._thdNoise = ThdNoise(self._core, self._cmd_group)
		return self._thdNoise

	# noinspection PyTypeChecker
	class SnRatioStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Enable_Left: bool: OFF | ON Enables or disables the limit check for the left SPDIF channel.
			- Lower_Left: float: Lower limit for the left SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB
			- Enable_Right: bool: OFF | ON Enables or disables the limit check for the right SPDIF channel.
			- Lower_Right: float: Lower limit for the right SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB
			- Upper_Left: float: Optional setting parameter. Upper limit for the left SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB
			- Upper_Right: float: Optional setting parameter. Upper limit for the right SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Lower_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Lower_Right'),
			ArgStruct.scalar_float_optional('Upper_Left'),
			ArgStruct.scalar_float_optional('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Lower_Left: float = None
			self.Enable_Right: bool = None
			self.Lower_Right: float = None
			self.Upper_Left: float = None
			self.Upper_Right: float = None

	def get_sn_ratio(self) -> SnRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNRatio \n
		Snippet: value: SnRatioStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.get_sn_ratio() \n
		Configures limits for all SNR results, measured via the SPDIF input path. SNR results include S/N, (S+N) /N and (S+N+D)
		/N. \n
			:return: structure: for return value, see the help for SnRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNRatio?', self.__class__.SnRatioStruct())

	def set_sn_ratio(self, value: SnRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNRatio \n
		Snippet with structure: \n
		structure = driver.configure.afRf.measurement.multiEval.limit.spdif.SnRatioStruct() \n
		structure.Enable_Left: bool = False \n
		structure.Lower_Left: float = 1.0 \n
		structure.Enable_Right: bool = False \n
		structure.Lower_Right: float = 1.0 \n
		structure.Upper_Left: float = 1.0 \n
		structure.Upper_Right: float = 1.0 \n
		driver.configure.afRf.measurement.multiEval.limit.spdif.set_sn_ratio(value = structure) \n
		Configures limits for all SNR results, measured via the SPDIF input path. SNR results include S/N, (S+N) /N and (S+N+D)
		/N. \n
			:param value: see the help for SnRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNRatio', value)

	# noinspection PyTypeChecker
	class SinadStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Enable_Left: bool: OFF | ON Enables or disables the limit check for the left SPDIF channel
			- Lower_Left: float: Lower SINAD limit for the left SPDIF channel Range: 0 dB to 140 dB, Unit: dB
			- Enable_Right: bool: OFF | ON Enables or disables the limit check for the right SPDIF channel
			- Lower_Right: float: Lower SINAD limit for the right SPDIF channel Range: 0 dB to 140 dB, Unit: dB
			- Upper_Left: float: Optional setting parameter. Upper SINAD limit for the left SPDIF channel Range: 0 dB to 140 dB, Unit: dB
			- Upper_Right: float: Optional setting parameter. Upper SINAD limit for the right SPDIF channel Range: 0 dB to 140 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Lower_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Lower_Right'),
			ArgStruct.scalar_float_optional('Upper_Left'),
			ArgStruct.scalar_float_optional('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Lower_Left: float = None
			self.Enable_Right: bool = None
			self.Lower_Right: float = None
			self.Upper_Left: float = None
			self.Upper_Right: float = None

	def get_sinad(self) -> SinadStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SINad \n
		Snippet: value: SinadStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.get_sinad() \n
		Configures limits for the SINAD results, measured via the SPDIF input path. \n
			:return: structure: for return value, see the help for SinadStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SINad?', self.__class__.SinadStruct())

	def set_sinad(self, value: SinadStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SINad \n
		Snippet with structure: \n
		structure = driver.configure.afRf.measurement.multiEval.limit.spdif.SinadStruct() \n
		structure.Enable_Left: bool = False \n
		structure.Lower_Left: float = 1.0 \n
		structure.Enable_Right: bool = False \n
		structure.Lower_Right: float = 1.0 \n
		structure.Upper_Left: float = 1.0 \n
		structure.Upper_Right: float = 1.0 \n
		driver.configure.afRf.measurement.multiEval.limit.spdif.set_sinad(value = structure) \n
		Configures limits for the SINAD results, measured via the SPDIF input path. \n
			:param value: see the help for SinadStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SINad', value)

	# noinspection PyTypeChecker
	class SnnRatioStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Enable_Left: bool: OFF | ON Enables or disables the limit check for the left SPDIF channel.
			- Lower_Left: float: Lower limit for the left SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB
			- Enable_Right: bool: OFF | ON Enables or disables the limit check for the right SPDIF channel.
			- Lower_Right: float: Lower limit for the right SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB
			- Upper_Left: float: Optional setting parameter. Upper limit for the left SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB
			- Upper_Right: float: Optional setting parameter. Upper limit for the right SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Lower_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Lower_Right'),
			ArgStruct.scalar_float_optional('Upper_Left'),
			ArgStruct.scalar_float_optional('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Lower_Left: float = None
			self.Enable_Right: bool = None
			self.Lower_Right: float = None
			self.Upper_Left: float = None
			self.Upper_Right: float = None

	def get_snn_ratio(self) -> SnnRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNNRatio \n
		Snippet: value: SnnRatioStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.get_snn_ratio() \n
		Configures limits for all SNR results, measured via the SPDIF input path. SNR results include S/N, (S+N) /N and (S+N+D)
		/N. \n
			:return: structure: for return value, see the help for SnnRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNNRatio?', self.__class__.SnnRatioStruct())

	def set_snn_ratio(self, value: SnnRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNNRatio \n
		Snippet with structure: \n
		structure = driver.configure.afRf.measurement.multiEval.limit.spdif.SnnRatioStruct() \n
		structure.Enable_Left: bool = False \n
		structure.Lower_Left: float = 1.0 \n
		structure.Enable_Right: bool = False \n
		structure.Lower_Right: float = 1.0 \n
		structure.Upper_Left: float = 1.0 \n
		structure.Upper_Right: float = 1.0 \n
		driver.configure.afRf.measurement.multiEval.limit.spdif.set_snn_ratio(value = structure) \n
		Configures limits for all SNR results, measured via the SPDIF input path. SNR results include S/N, (S+N) /N and (S+N+D)
		/N. \n
			:param value: see the help for SnnRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNNRatio', value)

	# noinspection PyTypeChecker
	class SndRatioStruct(StructBase):  # From WriteStructDefinition CmdPropertyTemplate.xml
		"""Structure for setting input parameters. Contains optional set arguments. Fields: \n
			- Enable_Left: bool: OFF | ON Enables or disables the limit check for the left SPDIF channel.
			- Lower_Left: float: Lower limit for the left SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB
			- Enable_Right: bool: OFF | ON Enables or disables the limit check for the right SPDIF channel.
			- Lower_Right: float: Lower limit for the right SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB
			- Upper_Left: float: Optional setting parameter. Upper limit for the left SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB
			- Upper_Right: float: Optional setting parameter. Upper limit for the right SPDIF channel Range: 0.00 dB to 140.00 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Lower_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Lower_Right'),
			ArgStruct.scalar_float_optional('Upper_Left'),
			ArgStruct.scalar_float_optional('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Lower_Left: float = None
			self.Enable_Right: bool = None
			self.Lower_Right: float = None
			self.Upper_Left: float = None
			self.Upper_Right: float = None

	def get_snd_ratio(self) -> SndRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNDRatio \n
		Snippet: value: SndRatioStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.get_snd_ratio() \n
		Configures limits for all SNR results, measured via the SPDIF input path. SNR results include S/N, (S+N) /N and (S+N+D)
		/N. \n
			:return: structure: for return value, see the help for SndRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNDRatio?', self.__class__.SndRatioStruct())

	def set_snd_ratio(self, value: SndRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNDRatio \n
		Snippet with structure: \n
		structure = driver.configure.afRf.measurement.multiEval.limit.spdif.SndRatioStruct() \n
		structure.Enable_Left: bool = False \n
		structure.Lower_Left: float = 1.0 \n
		structure.Enable_Right: bool = False \n
		structure.Lower_Right: float = 1.0 \n
		structure.Upper_Left: float = 1.0 \n
		structure.Upper_Right: float = 1.0 \n
		driver.configure.afRf.measurement.multiEval.limit.spdif.set_snd_ratio(value = structure) \n
		Configures limits for all SNR results, measured via the SPDIF input path. SNR results include S/N, (S+N) /N and (S+N+D)
		/N. \n
			:param value: see the help for SndRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNDRatio', value)

	def clone(self) -> 'Spdif':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Spdif(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
