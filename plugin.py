import sublime, sublime_plugin

from .app.logger import Logger
from .app.settings import Settings
from .app.logger_settings import updateLoggerSettings



class SublimeModelinesPlugin(sublime_plugin.EventListener):
	
	def __init__(self):
		super().__init__()
		updateLoggerSettings()
		Logger.debug("Plugin init.")
	
	def on_load(self, view):
		Logger.debug("on_load called.")
		#self.do_modelines(view)
	
	def on_post_save(self, view):
		Logger.debug("on_post_save called.")
		#self.do_modelines(view)
