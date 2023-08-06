from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 9 total commands, 6 Subgroups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("limit", core, parent)

	@property
	def tvaDelay(self):
		"""tvaDelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tvaDelay'):
			from .TvaDelay import TvaDelay
			self._tvaDelay = TvaDelay(self._core, self._cmd_group)
		return self._tvaDelay

	@property
	def rsensitivity(self):
		"""rsensitivity commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_rsensitivity'):
			from .Rsensitivity import Rsensitivity
			self._rsensitivity = Rsensitivity(self._core, self._cmd_group)
		return self._rsensitivity

	@property
	def rifBandwidth(self):
		"""rifBandwidth commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rifBandwidth'):
			from .RifBandwidth import RifBandwidth
			self._rifBandwidth = RifBandwidth(self._core, self._cmd_group)
		return self._rifBandwidth

	@property
	def rsquelch(self):
		"""rsquelch commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rsquelch'):
			from .Rsquelch import Rsquelch
			self._rsquelch = Rsquelch(self._core, self._cmd_group)
		return self._rsquelch

	@property
	def ssnr(self):
		"""ssnr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ssnr'):
			from .Ssnr import Ssnr
			self._ssnr = Ssnr(self._core, self._cmd_group)
		return self._ssnr

	@property
	def tsensitivity(self):
		"""tsensitivity commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_tsensitivity'):
			from .Tsensitivity import Tsensitivity
			self._tsensitivity = Tsensitivity(self._core, self._cmd_group)
		return self._tsensitivity

	def clone(self) -> 'Limit':
		"""Clones the group by creating new object from it and its whole existing subgroups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Limit(self._core, self._cmd_group.parent)
		self._cmd_group.synchronize_repcaps(new_group)
		return new_group
