import sublime, sublimeplugin

def getLineCommentCharacter(view):

    commentChar = ""

    try:
        for pair in view.metaInfo("shellVariables", 0):
            commentChar = pair["value"]
            if pair["name"] == "TM_COMMENT_START":
                break
    except TypeError:
        pass

    return commentChar.strip()


class ExecuteSublimeTextModeLinesCommand(sublimeplugin.Plugin):
    """
    This plugin provides a feature similar to vim modelines.
    Modelines set options local to the view by declaring them in the
    source code file itself.

        Example:
        mysourcecodefile.py
        # st: gutter false
        # st: autoIndent false

    Note that only the range spanning from 0 to MAX_LINES_TO_CHECK * LINE_LENGTH
    are searched for modelines.

    TODO: let user declare multiple options per line.
    TODO: let user declare modelines in block comments
    """
    SUBLIMETEXT_MODELINE_PREFIX_TPL = "%s st: "
    MAX_LINES_TO_CHECK = 50
    LINE_LENGTH = 80

    def _getModelineCandidates(self, view):

        boundary = min(self.MAX_LINES_TO_CHECK * self.LINE_LENGTH, view.size())
        candidates = view.splitByNewlines(sublime.Region(0, view.fullLine(boundary).end()))

        # Add region at bottom of file if the file is large enough.
        if boundary < view.size():
            # don't exceed view.size()
            upperBoundary = min(max(view.size() - boundary, candidates[-1].end() + 1),
                                view.size())

            bottomRegion = sublime.Region(upperBoundary, view.size())
            candidates += view.splitByNewlines(bottomRegion)

        return [candidate for candidate in candidates if not candidate.empty()]

    def _getOptionsToSet(self, view):

        opts = []
        actualPrefix = (self.SUBLIMETEXT_MODELINE_PREFIX_TPL %
                                # sometimes there is no line comment char, so
                                # st: should be right at the start of the line.
                                getLineCommentCharacter(view)).lstrip()

        for candidate in self._getModelineCandidates(view):

            candidateStr = view.substr(candidate)
            print candidateStr
            if candidateStr.startswith(actualPrefix):
                name, discard, value = candidateStr[len(actualPrefix):].partition(" ")
                opts.append((name, value))

        return opts

    def _setOptions(self, view):

        for name, value in self._getOptionsToSet(view):
            # spaces in options are illegal in sublime text
            view.options().set(name.strip(), value)

    def onLoad(self, view):
        self._setOptions(view)
