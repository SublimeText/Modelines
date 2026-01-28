import sys

from .logger import Logger
from .settings import Settings



def _updateLoggerSettings() -> None:
	settings = Settings()
	Logger.enable_debug_log = settings.verbose()
	Logger.log_to_tmp       = settings.log_to_tmp()

Logger.updateSettings = _updateLoggerSettings
