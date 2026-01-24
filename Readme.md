# Sublime Modelines

Set settings local to a single buffer.  
A more granular approach to settings than the per file type `.sublime-settings` files.

Inspired by Vim’s modelines feature.


## Getting Started

### Recommended Installation

Use Package Control and install `SublimeModelines`.

### Manual Installation

Download and install [SublimeModelines](<https://github.com/SublimeText/Modelines>).

See the [installation instructions](<https://docs.sublimetext.io/guide/extensibility/packages.html#installing-packages>) for `.sublime-package`s.


## Side Effects

Buffers will be scanned `.on_load()` for modelines and settings will be set accordingly.
Settings will apply **only** to the buffer declaring them.

**Note**: Application- and window-level options declared in modelines are obviously global.


## Usage

### How to Declare Modelines

Modelines must be declared at the top or the bottom of source code files with one of the following syntaxes:

```text
# sublime: option_name value
# sublime: option_name value; another_option value; third_option value
```

**Note**:
`#` is the default comment character.
Use the corresponding single-line comment character for your language.
When there isn't a concept of comment, the default comment character must be used.

### How to Define Comment Characters in Sublime Text

SublimeModelines finds the appropriate single-line comment character by inspecting the `shellVariables` preference,
 which must be defined in a `.tmPreferences` file.
To see an example of how this is done, open `Packages/Python/Miscellaneous.tmPreferences`.

Many packages giving support for programming languages already include this,
 but you might need to create a `.tmPreferences` file for the language you're working with
 if you want SublimeModelines to be available.
 

## Caveats

If the option’s value contains a semicolon (`;`), make sure it isn't followed by a blank space.
Otherwise it will be interpreted as a multi-option separator.


## Non-Standard Options

For some common cases, no directly settable option exists (for example, a setting to specify a syntax).
For such cases, Sublime Modelines provides non-standard accessors as a stop-gap solution.

```text
# sublime: x_syntax Foo
or
# sublime: x_syntax Packages/Foo/Foo.tmLanguage
```

Sets the syntax to the specified `.tmLanguage` file.


# Contributors

[Guillermo López-Anglada](<https://github.com/guillermooo>):
- Implemented the first version of this package (for Sublime Text 2).

Kay-Uwe (Kiwi) Lorenz <kiwi@franka.dyndns.org> (<http://quelltexter.org>):
- Added VIM compatibility;
- Smart syntax matching;
- Modelines also parsed on save;
- Settings are erased from view, if removed from modeline.

[Frizlab](<https://github.com/Frizlab>):
- Removed VIM compatibility (use `VimModelines` if you need that);
- Modernize/clean the project, and make sure it works with SublimeText 4.
