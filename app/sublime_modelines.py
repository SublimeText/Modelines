import re, sys, json, os


debug_log("Modelines plugin start.")


MODELINE_PREFIX_TPL = "%s\\s*(st|sublime):"

MODELINE_TYPE_1  = re.compile(r"[\x20\t](st|sublime):\x20?set\x20(.*):.*$")
MODELINE_TYPE_2  = re.compile(r"[\x20\t](st|sublime):(.*):.*$")

KEY_VALUE = re.compile(r"""(?x) \s*
    (?P<key>\w+)  \s* (?P<op>\+?=)  \s*  (?P<value>
        (?:  "(?:\\.|[^"\\])*"
            | [\[\{].*
            | [^\s:]+
            ))
    """)

KEY_ONLY  = re.compile(r"""(?x)\s*(?P<key>\w+)""")

DEFAULT_LINE_COMMENT = "#"
MULTIOPT_SEP = "; "
MAX_LINES_TO_CHECK = 50
LINE_LENGTH = 80
MODELINES_REG_SIZE = MAX_LINES_TO_CHECK * LINE_LENGTH

ST3 = sublime.version() >= "3000"

if ST3:
    basestring = str

def get_output_panel(name):
    if ST3: return sublime.active_window().create_output_panel(name)
    else:   return sublime.active_window().get_output_panel(name)

def is_modeline(prefix, line):
    return bool(re.match(prefix, line))

def gen_modelines(view):
    topRegEnd = min(MODELINES_REG_SIZE, view.size())
    candidates = view.lines(sublime.Region(0, view.full_line(topRegEnd).end()))

    # Consider modelines at the end of the buffer too.
    # There might be overlap with the top region, but it doesn’t matter because it means the buffer is tiny.
    bottomRegStart = view.size() - MODELINES_REG_SIZE
    if bottomRegStart < 0: bottomRegStart = 0

    candidates += view.lines(sublime.Region(bottomRegStart, view.size()))

    prefix = build_modeline_prefix(view)
    modelines = (view.substr(c) for c in candidates if is_modeline(prefix, view.substr(c)))

    for modeline in modelines:
        yield modeline


def gen_raw_options(modelines):
    #import spdb ; spdb.start()
    for m in modelines:
        match = MODELINE_TYPE_1.search(m)
        if not match:
            match = MODELINE_TYPE_2.search(m)
        
        if match:
            type, s = match.groups()
            
            while True:
                if s.startswith(":"): s = s[1:]
                
                m = KEY_VALUE.match(s)
                if m:
                    yield m.groups()
                    s = s[m.end():]
                    continue
                
                m = KEY_ONLY.match(s)
                if m:
                    k, = m.groups()
                    value = "true"
                    
                    yield k, "=", value
                    
                    s = s[m.end():]
                    continue
                
                break
            
            continue
        
        # Original sublime modelines style.
        opt = m.partition(":")[2].strip()
        if MULTIOPT_SEP in opt:
            for subopt in (s for s in opt.split(MULTIOPT_SEP)):
                yield subopt
        else:
            yield opt


def gen_modeline_options(view):
    modelines = gen_modelines(view)
    for opt in gen_raw_options(modelines):
        if not isinstance(opt, tuple):
            #import spdb ; spdb.start()
            name, sep, value = opt.partition(" ")
            yield view.settings().set, name.rstrip(":"), value.rstrip(";")
            
        else:
            name, op, value = opt
            
            def _setter(n,v):
                if op == "+=":
                    if v.startswith("{"):
                        default = {}
                    elif v.startswith("["):
                        default = []
                    elif isinstance(v, basestring):
                        default = ""
                    else:
                        default = 0
                    
                    ov = view.settings().get(n, default)
                    v = ov + v
                
                view.settings().set(n,v)
            
            yield _setter, name, value


def build_modeline_prefix(view):
    return (MODELINE_PREFIX_TPL % DEFAULT_LINE_COMMENT)


def to_json_type(v):
    """Convert string value to proper JSON type."""
    if not isinstance(v, str):
        return json.loads(json.dumps(v))
    
    try:
        return json.loads(v.strip())
    except Exception as e:
        if v:
            if v[0] not in "[{":
                return v
        raise ValueError("Could not convert from JSON: %s" % v)


class ExecuteSublimeTextModeLinesCommand(sublime_plugin.EventListener):
    """This plugin provides a feature similar to vim modelines.
    Modelines set options local to the view by declaring them in the source code file itself.
    
        Example:
        mysourcecodefile.py
        # sublime: gutter false
        # sublime: translate_tab_to_spaces true
    
    The top as well as the bottom of the buffer is scanned for modelines.
    MAX_LINES_TO_CHECK * LINE_LENGTH defines the size of the regions to be scanned.
    """
    
    settings = None
    
    def __init__(self):
        self._modes = {}
    
    def do_modelines(self, view):
        if not self._modes:
            self.init_syntax_files()
        
        settings = view.settings()
        
        ignored_packages = settings.get("ignored_packages")
        
        keys = set(settings.get("sublime_modelines_keys", []))
        new_keys = set()
        
        base_dir = settings.get("result_base_dir")
        
        for setter, name, value in gen_modeline_options(view):
            debug_log("modeline: %s = %s", name, value)
            
            if name == "x_syntax":
                syntax_file = None
                if value.lower() in self._modes: syntax_file = self._modes[value.lower()]
                else:                            syntax_file = value
                
                if ST3: view.assign_syntax(syntax_file)
                else:   view.set_syntax_file(syntax_file)
                
                new_keys.add("x_syntax")
                debug_log("set syntax = %s" % syntax_file)
                
            else:
                try:
                    setter(name, to_json_type(value))
                    new_keys.add(name)
                except ValueError as e:
                    sublime.status_message("[SublimeModelines] Bad modeline detected.")
                    log_to_console("Bad option detected: %s, %s.", name, value)
                    log_to_console("Tip: Keys cannot be empty strings.")
        
        for k in keys:
            if k not in new_keys:
                if settings.has(k):
                    settings.erase(k)
        
        settings.set("sublime_modelines_keys", list(new_keys))
    
    
    # From <https://github.com/kvs/STEmacsModelines>.
    def init_syntax_files(self):
        for syntax_file in self.find_syntax_files():
            name = os.path.splitext(os.path.basename(syntax_file))[0].lower()
            self._modes[name] = syntax_file
        
        # Load custom mappings from the settings file.
        self.settings = sublime.load_settings("SublimeModelines.sublime-settings")
        
        if self.settings.has("mode_mappings"):
            for modeline, syntax in self.settings.get("mode_mappings").items():
                self._modes[modeline] = self._modes[syntax.lower()]
        
        if self.settings.has("user_mode_mappings"):
            for modeline, syntax in self.settings.get("user_mode_mappings").items():
                self._modes[modeline] = self._modes[syntax.lower()]
    
    
    # From <https://github.com/kvs/STEmacsModelines>.
    def find_syntax_files(self):
        # ST3
        if hasattr(sublime, "find_resources"):
            for f in sublime.find_resources("*.tmLanguage"):
                yield f
            for f in sublime.find_resources("*.sublime-syntax"):
                yield f
        else:
            for root, dirs, files in os.walk(sublime.packages_path()):
                for f in files:
                    if f.endswith(".tmLanguage") or f.endswith("*.sublime-syntax"):
                        langfile = os.path.relpath(os.path.join(root, f), sublime.packages_path())
                        # ST2 (as of build 2181) requires unix/MSYS style paths for the “syntax” view setting.
                        yield os.path.join("Packages", langfile).replace("\\", "/")
