import sys

from .logger import Logger
from .settings import Settings



# This cannot be defined in Logger because we need to import Settings to implement the function, and Settings uses Logger…
def updateLoggerSettings(settings: Settings) -> None:
	Logger.enable_debug_log = settings.verbose()
	Logger.log_to_tmp       = settings.log_to_tmp()
