from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.Types import DataType
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from .......Internal.ArgSingleList import ArgSingleList
from .......Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Timeout:
	"""Timeout commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("timeout", core, parent)

	def set(self, enable: bool, timeout: float = None) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:TOUT \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.timeout.set(enable = False, timeout = 1.0) \n
		Configures a timeout for the trigger modes 'Single' and 'Normal'. \n
			:param enable: OFF | ON Enables the timeout
			:param timeout: Time interval during which a trigger event must occur Range: 0.2 s to 30 s, Unit: s
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('enable', enable, DataType.Boolean), ArgSingle('timeout', timeout, DataType.Float, None, is_optional=True))
		self._core.io.write(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:TOUT {param}'.rstrip())

	# noinspection PyTypeChecker
	class TimeoutStruct(StructBase):
		"""Response structure. Fields: \n
			- Enable: bool: OFF | ON Enables the timeout
			- Timeout: float: Time interval during which a trigger event must occur Range: 0.2 s to 30 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Timeout')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Timeout: float = None

	def get(self) -> TimeoutStruct:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:TOUT \n
		Snippet: value: TimeoutStruct = driver.trigger.afRf.measurement.multiEval.oscilloscope.timeout.get() \n
		Configures a timeout for the trigger modes 'Single' and 'Normal'. \n
			:return: structure: for return value, see the help for TimeoutStruct structure arguments."""
		return self._core.io.query_struct(f'TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:TOUT?', self.__class__.TimeoutStruct())
