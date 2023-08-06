from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Device:
	"""Device commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("device", core, parent)

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.ScreenshotFormat:
		"""SCPI: HCOPy:DEVice:FORMat \n
		Snippet: value: enums.ScreenshotFormat = driver.hardCopy.device.get_format_py() \n
		Specifies the format of screenshots created via a HCOPy command. \n
			:return: file_formats: BMP | JPG | PNG
		"""
		response = self._core.io.query_str('HCOPy:DEVice:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.ScreenshotFormat)

	def set_format_py(self, file_formats: enums.ScreenshotFormat) -> None:
		"""SCPI: HCOPy:DEVice:FORMat \n
		Snippet: driver.hardCopy.device.set_format_py(file_formats = enums.ScreenshotFormat.BMP) \n
		Specifies the format of screenshots created via a HCOPy command. \n
			:param file_formats: BMP | JPG | PNG
		"""
		param = Conversions.enum_scalar_to_str(file_formats, enums.ScreenshotFormat)
		self._core.io.write(f'HCOPy:DEVice:FORMat {param}')
