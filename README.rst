SublimeModelines package for Sublime Text
=========================================

Vim-like modelines for the Sublime Text editor. With this plugin you can apply settings to files selectively.

Side effects
************

All opened files will be scanned ``onLoad`` for modelines and settings defined in them will be applied. Other than that, there shouldn't be any side effects.

Usage
*****

How to declare modelines
------------------------

Modelines must be declared in source code files with one of the following syntaxes::

    # sublime: optionName value
    # st: optionName value

**Note**: ``#`` is the default comment character, but you must use the corresponding single-line commend character for your language. In cases where there isn't a concept of comment, the default one must be used.

Examples::
**********

    # sublime: drawWhiteSpace all
    # sublime: gutter false
    # sublime: translateTabsToSpaces false
    # sublime: font Comic Sans 8
