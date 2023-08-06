from typing import List

from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Types import DataType
from ...Internal.Utilities import trim_str_response
from ...Internal.ArgSingleList import ArgSingleList
from ...Internal.ArgSingle import ArgSingle


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MassMemory:
	"""MassMemory commands group definition. 17 total commands, 6 Subgroups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("massMemory", core, parent)

	@property
	def attribute(self):
		"""attribute commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_attribute'):
			from .Attribute import Attribute
			self._attribute = Attribute(self._core, self._cmd_group)
		return self._attribute

	@property
	def catalog(self):
		"""catalog commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_catalog'):
			from .Catalog import Catalog
			self._catalog = Catalog(self._core, self._cmd_group)
		return self._catalog

	@property
	def currentDirectory(self):
		"""currentDirectory commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_currentDirectory'):
			from .CurrentDirectory import CurrentDirectory
			self._currentDirectory = CurrentDirectory(self._core, self._cmd_group)
		return self._currentDirectory

	@property
	def dcatalog(self):
		"""dcatalog commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_dcatalog'):
			from .Dcatalog import Dcatalog
			self._dcatalog = Dcatalog(self._core, self._cmd_group)
		return self._dcatalog

	@property
	def load(self):
		"""load commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_load'):
			from .Load import Load
			self._load = Load(self._core, self._cmd_group)
		return self._load

	@property
	def store(self):
		"""store commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_store'):
			from .Store import Store
			self._store = Store(self._core, self._cmd_group)
		return self._store

	def copy(self, file_source: str, file_destination: str = None) -> None:
		"""SCPI: MMEMory:COPY \n
		Snippet: driver.massMemory.copy(file_source = '1', file_destination = '1') \n
		Copies an existing file. The target directory must exist. \n
			:param file_source: String parameter to specify the name of the file to be copied. Wildcards ? and * are allowed if FileDestination contains a path without file name.
			:param file_destination: String parameter to specify the path and/or name of the new file. If the parameter is omitted, the new file is written to the current directory (see method RsCma.MassMemory.CurrentDirectory.set) .
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('file_source', file_source, DataType.String), ArgSingle('file_destination', file_destination, DataType.String, None, is_optional=True))
		self._core.io.write(f'MMEMory:COPY {param}'.rstrip())

	def delete(self, filename: str) -> None:
		"""SCPI: MMEMory:DELete \n
		Snippet: driver.massMemory.delete(filename = '1') \n
		Deletes the specified files. \n
			:param filename: String parameter to specify the file to be deleted. The wildcards * and ? are allowed. Specifying a directory instead of a file is not allowed.
		"""
		param = Conversions.value_to_quoted_str(filename)
		self._core.io.write(f'MMEMory:DELete {param}')

	def get_drives(self) -> List[str]:
		"""SCPI: MMEMory:DRIVes \n
		Snippet: value: List[str] = driver.massMemory.get_drives() \n
		Returns a list of the drives of the instrument. \n
			:return: drive: No help available
		"""
		response = self._core.io.query_str('MMEMory:DRIVes?')
		return Conversions.str_to_str_list(response)

	def make_directory(self, directory_name: str) -> None:
		"""SCPI: MMEMory:MDIRectory \n
		Snippet: driver.massMemory.make_directory(directory_name = '1') \n
		Creates a directory. \n
			:param directory_name: String parameter to specify the new directory. All not yet existing parts of the specified path are created.
		"""
		param = Conversions.value_to_quoted_str(directory_name)
		self._core.io.write(f'MMEMory:MDIRectory {param}')

	def move(self, file_source: str, file_destination: str) -> None:
		"""SCPI: MMEMory:MOVE \n
		Snippet: driver.massMemory.move(file_source = '1', file_destination = '1') \n
		Moves an existing object (file or directory) to a new location and renames it. \n
			:param file_source: String parameter to specify the name of the object to be moved or renamed. Wildcards ? and * are allowed if the files are not renamed.
			:param file_destination: String parameter to specify the new name and/or path of the object. New object name without path: The object is renamed. New path without object name: The object is moved. New path and new object name: The object is moved and renamed.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('file_source', file_source, DataType.String), ArgSingle('file_destination', file_destination, DataType.String))
		self._core.io.write(f'MMEMory:MOVE {param}'.rstrip())

	def get_msis(self) -> str:
		"""SCPI: MMEMory:MSIS \n
		Snippet: value: str = driver.massMemory.get_msis() \n
		Sets the default storage unit to the specified drive or network server. When the default storage unit is changed, the R&S
		CMA180 checks whether the current directory (see method RsCma.MassMemory.CurrentDirectory.set) is also available on the
		new storage unit. If not, the current directory is automatically set to '/'. \n
			:return: msus: No help available
		"""
		response = self._core.io.query_str('MMEMory:MSIS?')
		return trim_str_response(response)

	def set_msis(self, msus: str) -> None:
		"""SCPI: MMEMory:MSIS \n
		Snippet: driver.massMemory.set_msis(msus = '1') \n
		Sets the default storage unit to the specified drive or network server. When the default storage unit is changed, the R&S
		CMA180 checks whether the current directory (see method RsCma.MassMemory.CurrentDirectory.set) is also available on the
		new storage unit. If not, the current directory is automatically set to '/'. \n
			:param msus: String parameter to specify the default storage unit. If the parameter is omitted, the storage unit is set to D:.
		"""
		param = Conversions.value_to_quoted_str(msus)
		self._core.io.write(f'MMEMory:MSIS {param}')

	def delete_directory(self, directory_name: str) -> None:
		"""SCPI: MMEMory:RDIRectory \n
		Snippet: driver.massMemory.delete_directory(directory_name = '1') \n
		Deletes an existing empty directory. \n
			:param directory_name: String parameter to specify the directory.
		"""
		param = Conversions.value_to_quoted_str(directory_name)
		self._core.io.write(f'MMEMory:RDIRectory {param}')

	def clone(self) -> 'MassMemory':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MassMemory(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
