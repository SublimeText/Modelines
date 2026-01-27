import sys



class Logger:
	"""A simple logger."""
	
	# Default config for the logger.
	# Regarding the logging to a tmp file, this dates back to a time where I did not know how to show the console in Sublime (ctrl-`).
	# I used to log to a temporary file that I tailed.
	# Now this should probably always be False.
	enable_debug_log = False
	log_to_tmp = False
	
	def __new__(cls, *args, **kwargs):
		raise RuntimeError("Logger is static and thus cannot be instantiated.")
	
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
