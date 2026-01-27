import sys

from .settings import Settings



class Logger:
	"""A simple logger."""
	
	enable_debug_log = False
	log_to_tmp = False
	
	@staticmethod
	def updateSettings() -> None:
		settings = Settings()
		Logger.enable_debug_log = settings.verbose()
		Logger.log_to_tmp       = settings.log_to_tmp()
	
	@staticmethod
	def debug(s: str, *args) -> None:
		if not Logger.enable_debug_log:
			return
		Logger._log(Logger._format("", s, *args))
	
	@staticmethod
	def info(s: str, *args) -> None:
		Logger._log(Logger._format("", s, *args))
	
	@staticmethod
	def warning(s: str, *args) -> None:
		Logger._log(Logger._format("*** ", s, *args))
	
	@staticmethod
	def _format(prefix: str, s: str, *args) -> str:
		return "[Sublime Modelines] " + prefix + (s % args) + "\n"
	
	@staticmethod
	def _log(str: str) -> None:
		if Logger.log_to_tmp:
			with open("/tmp/sublime_modelines_debug.log", "a") as myfile:
				myfile.write(str)
		sys.stderr.write(str)
	
	def __new__(cls, *args, **kwargs):
		raise RuntimeError("Logger is static and thus cannot be instantiated.")
