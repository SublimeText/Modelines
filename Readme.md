# Modelines

Set settings local to a single buffer.  
A more granular approach to settings than the per file type `.sublime-settings` files.

Inspired by Vim’s modelines feature.


## Getting Started

### Recommended Installation

Use Package Control and install `Modelines` (compatibility starts at Sublime Text 4).

### Manual Installation

Download and install [Modelines](<https://github.com/SublimeText/Modelines>).

See the [installation instructions](<https://docs.sublimetext.io/guide/extensibility/packages.html#installing-packages>) for `.sublime-package`s.


## Side Effects

Buffers will be scanned `.on_load()` and `.on_post_save()` (by default, customizable) for modelines and settings will be set accordingly.
Settings will apply **only** to the buffer declaring them.

There is also a command to manually apply modelines.

**Note**: Application- and window-level options declared in modelines are obviously global.


## Usage

### How to Declare Modelines

Modelines must be declared at the top or the bottom of source code files with the following default syntax:

```text
# ~*~ sublime: key=val; key2=val2; key3 ~*~
```

VIM and Emacs-style syntax are also supported.  
See the settings file for (a lot) more info.


## Example

This is a simple example, that disable tabs auto-translation to spaces, set the tab size to 3 and set the file syntax to Python.

```text
# ~*~ sublime: syntax=Python; tab_size=3; translate_tabs_to_spaces=false ~*~
```

## Developer Note

To get proper completion and errors in the editor when working on this repo,
 one can create a `pyrightconfig.json` file at the root of the repo,
 containing something like this (on macOS; adjust paths accordingly depending on your environment):
```json
{
  "venvPath": ".",
  "venv": "sublime-modelines",
  "extraPaths": [
    "/Applications/Sublime Text.app/Contents/MacOS/Lib/python38",
    "/Users/YOUR_USER_NAME/Library/Application Support/Sublime Text/Lib/python38",
  ]
}
```

⚠️ The tests require the `UnitTesting` package.
I have not added it to `dependencies.json` because I don’t know how to add a dependency for tests only.
A PR is welcome if there is a way to do it.


# Contributors

## [François Lamboley (Frizlab)](<https://github.com/Frizlab>)

Full rewrite featuring:
- Sublime Text 4 compatibility;
- A whole new modeline syntax;
- Better VIM syntax support;
- Emacs syntax support;
- Legacy syntax support (original modeline syntax from this repo, before the rewrite).


## [Kay-Uwe (Kiwi) Lorenz](<http://quelltexter.org>) <kiwi@franka.dyndns.org>

- Added VIM compatibility;
- Smart syntax matching;
- Modelines also parsed on save;
- Settings are erased from view, if removed from modeline.


## [Guillermo López-Anglada](<https://github.com/guillermooo>)

- Implemented the first version of this package (for Sublime Text 2).
