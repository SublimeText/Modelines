import sys



class Logger:
	"""A simple logger."""
	
	# Default config for the logger.
	log_to_tmp = False
	enable_debug_log = False
	
	def __init__(self):
		super().__init__()
	
	def debug(self, s, *args):
		if not self.enable_debug_log:
			return
		self._log(self._format(s, *args))

	def info(self, s, *args):
		self._log(self._format(s, *args))
	
	def _format(self, s, *args):
		return "[SublimeModelines] " + (s % args) + "\n"
	
	def _log(self, str):
		if self.log_to_tmp:
			with open("/tmp/sublime_modelines_debug.log", "a") as myfile:
				myfile.write(str)
		sys.stderr.write(str)
