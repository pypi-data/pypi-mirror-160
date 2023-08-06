from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class SysSound:
	"""SysSound commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("sysSound", core, parent)

	def get_volume(self) -> int or bool:
		"""SCPI: CONFigure:BASE:SYSSound:VOLume \n
		Snippet: value: int or bool = driver.configure.base.sysSound.get_volume() \n
		Configures the volume of the system sound. \n
			:return: ssound: (integer or boolean) OFF Switches off the system sound without changing the volume setting ON Switches on the system sound without changing the volume setting number A number greater than zero sets the volume and switches on the system sound. Zero sets the volume and switches off the system sound. Range: 0 % to 100 %, Unit: %
		"""
		response = self._core.io.query_str('CONFigure:BASE:SYSSound:VOLume?')
		return Conversions.str_to_int_or_bool(response)

	def set_volume(self, ssound: int or bool) -> None:
		"""SCPI: CONFigure:BASE:SYSSound:VOLume \n
		Snippet: driver.configure.base.sysSound.set_volume(ssound = 1) \n
		Configures the volume of the system sound. \n
			:param ssound: (integer or boolean) OFF Switches off the system sound without changing the volume setting ON Switches on the system sound without changing the volume setting number A number greater than zero sets the volume and switches on the system sound. Zero sets the volume and switches off the system sound. Range: 0 % to 100 %, Unit: %
		"""
		param = Conversions.decimal_or_bool_value_to_str(ssound)
		self._core.io.write(f'CONFigure:BASE:SYSSound:VOLume {param}')
