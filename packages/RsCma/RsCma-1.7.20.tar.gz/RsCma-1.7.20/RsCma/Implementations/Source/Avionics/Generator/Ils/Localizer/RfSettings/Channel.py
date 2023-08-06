from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.Types import DataType
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct
from ........Internal.ArgSingleList import ArgSingleList
from ........Internal.ArgSingle import ArgSingle
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Channel:
	"""Channel commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("channel", core, parent)

	def set(self, channel: int, letter: enums.IlsLetter) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:CHANnel \n
		Snippet: driver.source.avionics.generator.ils.localizer.rfSettings.channel.set(channel = 1, letter = enums.IlsLetter.X) \n
		Selects the RF channel. Each channel is identified via a number and a letter, for example 18X. \n
			:param channel: Channel number Range: 18 to 56
			:param letter: X | Y Channel letter
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('channel', channel, DataType.Integer), ArgSingle('letter', letter, DataType.Enum, enums.IlsLetter))
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:CHANnel {param}'.rstrip())

	# noinspection PyTypeChecker
	class ChannelStruct(StructBase):
		"""Response structure. Fields: \n
			- Channel: int: Channel number Range: 18 to 56
			- Letter: enums.IlsLetter: X | Y Channel letter"""
		__meta_args_list = [
			ArgStruct.scalar_int('Channel'),
			ArgStruct.scalar_enum('Letter', enums.IlsLetter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Channel: int = None
			self.Letter: enums.IlsLetter = None

	def get(self) -> ChannelStruct:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:CHANnel \n
		Snippet: value: ChannelStruct = driver.source.avionics.generator.ils.localizer.rfSettings.channel.get() \n
		Selects the RF channel. Each channel is identified via a number and a letter, for example 18X. \n
			:return: structure: for return value, see the help for ChannelStruct structure arguments."""
		return self._core.io.query_struct(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:CHANnel?', self.__class__.ChannelStruct())
