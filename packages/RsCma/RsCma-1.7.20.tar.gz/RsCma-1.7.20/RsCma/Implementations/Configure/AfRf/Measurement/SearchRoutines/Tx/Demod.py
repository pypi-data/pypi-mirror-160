from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demod:
	"""Demod commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("demod", core, parent)

	# noinspection PyTypeChecker
	def get_scheme(self) -> enums.Demodulation:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:DEMod:SCHeme \n
		Snippet: value: enums.Demodulation = driver.configure.afRf.measurement.searchRoutines.tx.demod.get_scheme() \n
		Selects the type of demodulation to be performed. \n
			:return: scheme: FMSTereo | FM | AM | USB | LSB | PM FMSTereo FM stereo multiplex signal FM, PM, AM Frequency / phase / amplitude modulation USB, LSB Single sideband modulation, upper / lower sideband
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:DEMod:SCHeme?')
		return Conversions.str_to_scalar_enum(response, enums.Demodulation)

	def set_scheme(self, scheme: enums.Demodulation) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:DEMod:SCHeme \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.tx.demod.set_scheme(scheme = enums.Demodulation.AM) \n
		Selects the type of demodulation to be performed. \n
			:param scheme: FMSTereo | FM | AM | USB | LSB | PM FMSTereo FM stereo multiplex signal FM, PM, AM Frequency / phase / amplitude modulation USB, LSB Single sideband modulation, upper / lower sideband
		"""
		param = Conversions.enum_scalar_to_str(scheme, enums.Demodulation)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:SROutines:TX:DEMod:SCHeme {param}')
