import sublime, sublimeplugin

def getLineCommentCharacter(view):
    return (view.metaInfo("shellVariables", 0) or {}).get("TM_COMMENT_START", "")

class ExecuteSublimeTextModeLinesCommand(sublimeplugin.TextCommand):
    """
    This plugin provides a feature similar to vim modelines.
    Modelines set options local to the view by declaring them in the
    source code file itself.

        Example:
        mysourcecodefile.py
        # st: gutter false
        # st: autoIndent false

    Note that only MAX_LINES_TO_CHECK are searched for modelines.

    TODO: let user declare multiple options per line.
    TODO: some options will fail (rulers).
    TODO: use each language's single-line comment character in
    SUBLIMETEXT_MODELINE_PREFIX.
    """
    SUBLIMETEXT_MODELINE_PREFIX = "# st: "
    MAX_LINES_TO_CHECK = 50

    def _getAllLines(self, view):
        r = sublime.Region(0, view.size())
        return view.splitByNewlines(r)

    def _getModelineCandidates(self, view):
        ls = self._getAllLines(view)

        endPoint = ls[ min(self.MAX_LINES_TO_CHECK, len(ls)) - 1 ].end()
        modelinesRegion = sublime.Region(0, endPoint)

        return view.substr(modelinesRegion).split('\n')

    def run(self, view, args):
        print getLineCommentCharacter(view)

    def onLoad(self, view):
        whereOptionStarts = len(self.SUBLIMETEXT_MODELINE_PREFIX)

        for l in self._getModelineCandidates(view):

            if l.startswith(self.SUBLIMETEXT_MODELINE_PREFIX):
                try:
                    name, value = l[whereOptionStarts:].split(' ', 1)
                except ValueError:
                    print "Modeline syntax error:", l

                view.options().set(name, value)