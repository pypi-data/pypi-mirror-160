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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:GCOupling \n
		Snippet: driver.configure.afRf.measurement.spdif.gcoupling.set(coupling_left = enums.GeneratorCoupling.GEN1, coupling_right = enums.GeneratorCoupling.GEN1) \n
		Couples the channels of the SPDIF IN connector to an internal signal generator. The combinations GEN1+GEN4 and GEN3+GEN2
		are not allowed. \n
			:param coupling_left: OFF | GEN1 | GEN3 OFF No coupling of left channel GENn Left channel coupled to audio generator n
			:param coupling_right: OFF | GEN2 | GEN4 OFF No coupling of right channel GENn Right channel coupled to audio generator n
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('coupling_left', coupling_left, DataType.Enum, enums.GeneratorCoupling), ArgSingle('coupling_right', coupling_right, DataType.Enum, enums.GeneratorCoupling))
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SIN:GCOupling {param}'.rstrip())

	# noinspection PyTypeChecker
	class GcouplingStruct(StructBase):
		"""Response structure. Fields: \n
			- Coupling_Left: enums.GeneratorCoupling: OFF | GEN1 | GEN3 OFF No coupling of left channel GENn Left channel coupled to audio generator n
			- Coupling_Right: enums.GeneratorCoupling: OFF | GEN2 | GEN4 OFF No coupling of right channel GENn Right channel coupled to audio generator n"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Coupling_Left', enums.GeneratorCoupling),
			ArgStruct.scalar_enum('Coupling_Right', enums.GeneratorCoupling)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Coupling_Left: enums.GeneratorCoupling = None
			self.Coupling_Right: enums.GeneratorCoupling = None

	def get(self) -> GcouplingStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:GCOupling \n
		Snippet: value: GcouplingStruct = driver.configure.afRf.measurement.spdif.gcoupling.get() \n
		Couples the channels of the SPDIF IN connector to an internal signal generator. The combinations GEN1+GEN4 and GEN3+GEN2
		are not allowed. \n
			:return: structure: for return value, see the help for GcouplingStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:AFRF:MEASurement<Instance>:SIN:GCOupling?', self.__class__.GcouplingStruct())
