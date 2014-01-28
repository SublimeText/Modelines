# vim:et:ai:ts=4:syn=python:

import sublime, sublime_plugin
import re, sys, json, os

MODELINE_PREFIX_TPL = "%s\\s*(st|sublime|vim):"

MODELINE_TYPE_1  = re.compile(r"[\x20\t](st|sublime|vim):\x20?set\x20(.*):.*$")
MODELINE_TYPE_2  = re.compile(r"[\x20\t](st|sublime|vim):(.*):.*$")

KEY_VALUE = re.compile(r"""(?x) \s*
    (?P<key>\w+)  \s* (?P<op>\+?=)  \s*  (?P<value>
        (?:  "(?:\\.|[^"\\])*"
            | [\[\{].*
            | [^\s:]+
            ))
    """)

KEY_ONLY  = re.compile(r"""(?x)\s*(?P<key>\w+)""")

DEFAULT_LINE_COMMENT = '#'
MULTIOPT_SEP = '; '
MAX_LINES_TO_CHECK = 50
LINE_LENGTH = 80
ODELINES_REG_SIZE = MAX_LINES_TO_CHECK * LINE_LENGTH

MONITORED_OUTPUT_PANELS = ['exec']

ST3 = sublime.version() >= '3000'

if ST3:
    basestring = str

VIM_MAP = {
    #"gfn": "guifont"
    #"guifont": {"regex": ..., 1: "font_face", 2: ("font_size", int)}

    "ts": "tabstop",
    "tabstop": ("tab_size", int),
    "ai": "autoindent",
    "autoindent": ("auto_indent", bool),
    "et": "expandtab",
    "expandtab": ("translate_tabs_to_spaces", bool),
    "syn": "syntax",
    "syntax": ("syntax", str),
    "nu": "number",
    "number": ("line_numbers", bool),

    # "always_show_minimap_viewport": false,
    # "animation_enabled": true,
    # "atomic_save": true,
    # "auto_close_tags": true,
    # "auto_complete": true,
    # "auto_complete_commit_on_tab": false,
    # "auto_complete_delay": 50,
    # "auto_complete_selector": "source - comment, meta.tag - punctuation.definition.tag.begin",
    # "auto_complete_size_limit": 4194304,
    # "auto_complete_triggers": [ {"selector": "text.html", "characters": "<"} ],
    # "auto_complete_with_fields": false,
    # "auto_find_in_selection": false,
    # "auto_indent": true,
    # "auto_match_enabled": true,
    # "binary_file_patterns": ["*.jpg", "*.jpeg", "*.png", "*.gif", "*.ttf", "*.tga", "*.dds", "*.ico", "*.eot", "*.pdf", "*.swf", "*.jar", "*.zip"],
    # "bold_folder_labels": false,
    # "caret_style": "smooth",
    # "color_scheme": "Packages/Color Scheme - Default/Monokai.tmTheme",
    # "copy_with_empty_selection": true,
    # "default_encoding": "UTF-8",
    # "default_line_ending": "system",
    # "detect_indentation": true,
    # "dictionary": "Packages/Language - English/en_US.dic",
    # "drag_text": true,
    # "draw_centered": false,
    # "draw_indent_guides": true,
    # "draw_minimap_border": false,
    # "draw_white_space": "selection",
    # "enable_hexadecimal_encoding": true,
    # "enable_telemetry": "auto",
    # "ensure_newline_at_eof_on_save": false,
    # "fade_fold_buttons": true,
    # "fallback_encoding": "Western (Windows 1252)",
    # "file_exclude_patterns": ["*.pyc", "*.pyo", "*.exe", "*.dll", "*.obj","*.o", "*.a", "*.lib", "*.so", "*.dylib", "*.ncb", "*.sdf", "*.suo", "*.pdb", "*.idb", ".DS_Store", "*.class", "*.psd", "*.db", "*.sublime-workspace"],
    # "find_selected_text": true,
    # "fold_buttons": true,
    # "folder_exclude_patterns": [".svn", ".git", ".hg", "CVS"],
    # "font_face": "",
    # "font_options": [], # list
    # "font_size": 10,
    # "gpu_window_buffer": "auto",
    # "gutter": true,
    # "highlight_line": false,
    # "highlight_modified_tabs": false,
    # "ignored_packages": ["Vintage"]
    # "indent_guide_options": ["draw_normal"],
    # "indent_subsequent_lines": true,
    # "indent_to_bracket": false,
    # "index_files": true,
    # "line_padding_bottom": 0,
    # "line_padding_top": 0,
    # "margin": 4,
    # "match_brackets": true,
    # "match_brackets_angle": false,
    # "match_brackets_braces": true,
    # "match_brackets_content": true,
    # "match_brackets_square": true,
    # "match_selection": true,
    # "match_tags": true,
    # "move_to_limit_on_up_down": false,
    # "overlay_scroll_bars": "system",
    # "preview_on_click": true,
    # "rulers": [], # list
    # "save_on_focus_lost": false,
    # "scroll_past_end": true,
    # "scroll_speed": 1.0,
    # "shift_tab_unindent": false,
    # "show_panel_on_build": true,
    # "show_tab_close_buttons": true,
    # "smart_indent": true,
    # "spell_check": false,
    # "tab_completion": true,
    # "tab_size": 4,
    # "theme": "Default.sublime-theme",
    # "translate_tabs_to_spaces": false,
    # "tree_animation_enabled": true,
    # "trim_automatic_white_space": true,
    # "trim_trailing_white_space_on_save": false,
    # "use_simple_full_screen": false,
    # "use_tab_stops": true,
    # "word_separators": "./\\()\"'-:,.;<>~!@#$%^&*|+=[]{}`~?",
    # "word_wrap": "auto",
    # "wrap_width": 0,
}

def console_log(s, *args):
    sys.stderr.write('[SublimeModelines] '+(s % args)+"\n")

def get_language_files(ignored_packages, *paths):
    paths = list(paths)
    tml_files = []
    if ST3:kj
        tml_files.extend(sublime.find_resources('*.tmLanguage'))
    else:
        paths.insert(0, sublime.packages_path())

    for path in paths:
        for dir, dirs, files in os.walk(path):
            # TODO: be sure that not tmLanguage from disabled package is taken
            for fn in files:
                if fn.endswith('.tmLanguage'):
                    tml_files.append(os.path.join(dir, fn))

    R = re.compile("Packages[\\/]([^\\/]+)[\\/]")
    result = []
    for f in tml_files:
        m = R.search(f)
        if m:
            if m.group(1) not in ignored_packages:
                result.append(f)

    return result

def get_output_panel(name):
    if ST3: 
        return sublime.active_window().create_output_panel(name)
    else:
        return sublime.active_window().get_output_panel(name)

def is_modeline(prefix, line):
    return bool(re.match(prefix, line))


def gen_modelines(view):
    topRegEnd = min(MODELINES_REG_SIZE, view.size())
    candidates = view.lines(sublime.Region(0, view.full_line(topRegEnd).end()))

    # Consider modelines at the end of the buffer too.
    # There might be overlap with the top region, but it doesn't matter because
    # it means the buffer is tiny.
    bottomRegStart = filter(lambda x: x > -1,
                                ((view.size() - MODELINES_REG_SIZE), 0))

    bottomRegStart = view.size() - MODELINES_REG_SIZE

    if bottomRegStart < 0: bottomRegStart = 0

    candidates += view.lines( sublime.Region(bottomRegStart, view.size()) )

    prefix = build_modeline_prefix(view)
    modelines = (view.substr(c) for c in candidates if is_modeline(prefix, view.substr(c)))

    for modeline in modelines:
        yield modeline

def vim_mapped(t, s):
    if t == 'vim' or len(s) < 3:
        while s in VIM_MAP:
            s = VIM_MAP[s]
        return s[0]
    else:
        return s


def gen_raw_options(modelines):
    #import spdb ; spdb.start()
    for m in modelines:
        match = MODELINE_TYPE_1.search(m)
        if not match:
            match = MODELINE_TYPE_2.search(m)

        if match:
            type, s = match.groups()

            while True:
                if s.startswith(':'): s = s[1:]

                m = KEY_VALUE.match(s)
                if m:
                    key, op, value = m.groups()
                    yield vim_mapped(type, key), op, value
                    s = s[m.end():]
                    continue

                m = KEY_ONLY.match(s)
                if m:
                    k, = m.groups()
                    value = "true"

                    _k = vim_mapped(type, k)
                    if (k.startswith('no') and (type == 'vim' or (
                        k[2:] in VIM_MAP or len(k) <= 4))):

                        value = "false"
                        _k = vim_mapped(type, k[2:])

                    yield _k, '=', value

                    s = s[m.end():]
                    continue

                break

            continue

        # original sublime modelines style
        opt = m.partition(':')[2].strip()
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
            name, sep, value = opt.partition(' ')
            yield view.settings().set, name.rstrip(':'), value.rstrip(';')

        else:
            name, op, value = opt

            def _setter(n,v):
                if op == '+=':
                    if v.startswith('{'):
                        default = {}
                    elif v.startswith('['):
                        default = []
                    elif isinstance(v, basestring):
                        default = ""
                    else:
                        default = 0

                    ov = view.settings().get(n, default)
                    v = ov + v

                view.settings().set(n,v)

            yield _setter, name, value


def get_line_comment_char(view):
    commentChar = ""
    commentChar2 = ""
    try:
        for pair in view.meta_info("shellVariables", 0):
            if pair["name"] == "TM_COMMENT_START":
                commentChar = pair["value"]
            if pair["name"] == "TM_COMMENT_START_2":
                commentChar2 = pair["value"]
            if commentChar and commentChar2:
                break
    except TypeError:
        pass

    if not commentChar2:
        return re.escape(commentChar.strip())
    else:
        return "(" + re.escape(commentChar.strip()) + "|" + re.escape(commentChar2.strip()) + ")"

def build_modeline_prefix(view):
    lineComment = get_line_comment_char(view).lstrip() or DEFAULT_LINE_COMMENT
    return (MODELINE_PREFIX_TPL % lineComment)


def to_json_type(v):
    """"Convert string value to proper JSON type.
    """
    try:
        result = json.loads(v.strip())
        console_log("json: %s -> %s" % (v, repr(result)))
        return result
    except Exception as e:
        console_log("json: %s\n" % e)
        if v:
            if v[0] not in "[{":
                console_log("json: %s -> %s" % (v, repr(v)))
                return v
        raise ValueError("Could not convert from JSON: %s" % v)


class ExecuteSublimeTextModeLinesCommand(sublime_plugin.EventListener):
    """This plugin provides a feature similar to vim modelines.
    Modelines set options local to the view by declaring them in the
    source code file itself.

        Example:
        mysourcecodefile.py
        # sublime: gutter false
        # sublime: translate_tab_to_spaces true

    The top as well as the bottom of the buffer is scanned for modelines.
    MAX_LINES_TO_CHECK * LINE_LENGTH defines the size of the regions to be
    scanned.
    """
    def do_modelines(self, view):
        settings = view.settings()

        ignored_packages = settings.get('ignored_packages')

        keys = set(settings.get('sublime_modelines_keys', []))
        new_keys = set()

        base_dir = settings.get('result_base_dir')

        sys.stderr.write("do_modelines\n")

        for setter, name, value in gen_modeline_options(view):
            #if 'vim' in MODELINE_PREFIX_TPL: # vimsupport
            #    vim_map.get(name)
            console_log("modeline: %s = %s" % (name, value))

            if name in ('x_syntax', 'syntax'):
                syntax_file = None

                if os.path.isabs(value):
                    syntax_file = value

                    if not os.path.exists(syntax_file):
                        console_log("%s does not exist", value)
                        continue

                else:
                    # be smart about syntax:
                    if base_dir: 
                        lang_files = get_language_files(ignored_packages, base_dir)
                    else:
                        lang_files = get_language_files(ignored_packages)

                    #lang_files.sort(key=lambda x: len(os.path.basename(x)))

                    candidates = []
                    for syntax_file in lang_files:
                        if value in os.path.basename(syntax_file):
                            candidates.append(syntax_file)

                    value_lower = value.lower()
                    if not candidates:
                        for syntax_file in lang_files:
                            if value_lower in os.path.basename(syntax_file).lower():
                                candidates.append(syntax_file)

                    if not candidates:
                        console_log("%s cannot be resolved to a syntaxfile", value)
                        syntax_file = None
                        continue

                    else:
                        candidates.sort(key=lambda x: len(os.path.basename(x)))
                        syntax_file = candidates[0]

                if ST3:
                    view.assign_syntax(syntax_file)
                else:
                    view.set_syntax_file(syntax_file)

                new_keys.add('syntax')
                console_log("set syntax = %s" % syntax_file)

            else:
                try:
                    setter(name, to_json_type(value))
                    new_keys.add(name)
                except ValueError as e:
                    sublime.status_message("[SublimeModelines] Bad modeline detected.")
                    console_log("Bad option detected: %s, %s", name, value)
                    console_log("Tip: Keys cannot be empty strings.")

        for k in keys:
            if k not in new_keys:
                if settings.has(k):
                    settings.erase(k)

        settings.set('sublime_modelines_keys', list(new_keys))


    def on_load(self, view):
        self.do_modelines(view)

    def on_post_save(self, view):
        self.do_modelines(view)

    if 0:
      def on_modified(self, view):
        for p in MONITORED_OUTPUT_PANELS:
            v = get_output_panel(p)
            if v.id() != view.id(): continue
            return

            self.do_modelines(view)
            return
