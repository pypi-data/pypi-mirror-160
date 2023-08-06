from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ......Internal.ArgSingleList import ArgSingleList
from ......Internal.ArgSingle import ArgSingle
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gcoupling:
	"""Gcoupling commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("gcoupling", core, parent)

	def set(self, coupling_left: enums.GeneratorCoupling, coupling_right: enums.GeneratorCoupling) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:GCOupling \n
		Snippet: driver.configure.afRf.measurement.demodulation.gcoupling.set(coupling_left = enums.GeneratorCoupling.GEN1, coupling_right = enums.GeneratorCoupling.GEN1) \n
		Couples the audio output paths of the demodulator to an internal signal generator.
			INTRO_CMD_HELP: For FM stereo, the settings configure the left and the right audio channel. Only the following combinations are allowed: \n
			- OFF, OFF
			- GEN1, GEN2
			- GEN3, GEN4
		For other modulation types, only <CouplingLeft> is relevant. <CouplingRight> has no effect. \n
			:param coupling_left: OFF | GEN1 | GEN2 | GEN3 | GEN4 OFF No coupling GENn Coupled to audio generator n
			:param coupling_right: OFF | GEN2 | GEN4
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('coupling_left', coupling_left, DataType.Enum, enums.GeneratorCoupling), ArgSingle('coupling_right', coupling_right, DataType.Enum, enums.GeneratorCoupling))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:GCOupling {param}'.rstrip())

	# noinspection PyTypeChecker
	class GcouplingStruct(StructBase):
		"""Response structure. Fields: \n
			- Coupling_Left: enums.GeneratorCoupling: OFF | GEN1 | GEN2 | GEN3 | GEN4 OFF No coupling GENn Coupled to audio generator n
			- Coupling_Right: enums.GeneratorCoupling: OFF | GEN2 | GEN4"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Coupling_Left', enums.GeneratorCoupling),
			ArgStruct.scalar_enum('Coupling_Right', enums.GeneratorCoupling)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Coupling_Left: enums.GeneratorCoupling = None
			self.Coupling_Right: enums.GeneratorCoupling = None

	def get(self) -> GcouplingStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:GCOupling \n
		Snippet: value: GcouplingStruct = driver.configure.afRf.measurement.demodulation.gcoupling.get() \n
		Couples the audio output paths of the demodulator to an internal signal generator.
			INTRO_CMD_HELP: For FM stereo, the settings configure the left and the right audio channel. Only the following combinations are allowed: \n
			- OFF, OFF
			- GEN1, GEN2
			- GEN3, GEN4
		For other modulation types, only <CouplingLeft> is relevant. <CouplingRight> has no effect. \n
			:return: structure: for return value, see the help for GcouplingStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation:GCOupling?', self.__class__.GcouplingStruct())
