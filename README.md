# VimModelines for Sublime Text 3

[![Build Status](https://travis-ci.org/pestilence669/VimModelines.svg?branch=master)](https://travis-ci.org/pestilence669/VimModelines)
[![Build Status](https://ci.appveyor.com/api/projects/status/2uxv2kypphffxo2y/branch/master?svg=true)](https://ci.appveyor.com/project/pestilence669/vimmodelines/branch/master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0a3635083d0b4ddd99383406b4a18d41)](https://www.codacy.com/app/pestilence669/VimModelines?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=pestilence669/VimModelines&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/0a3635083d0b4ddd99383406b4a18d41)](https://www.codacy.com/app/pestilence669/VimModelines?utm_source=github.com&utm_medium=referral&utm_content=pestilence669/VimModelines&utm_campaign=Badge_Coverage)
[![codecov](https://codecov.io/gh/pestilence669/VimModelines/branch/master/graph/badge.svg)](https://codecov.io/gh/pestilence669/VimModelines)
[![packagecontrol.io Badge](https://packagecontrol.herokuapp.com/downloads/VimModelines.svg)](https://packagecontrol.io/packages/VimModelines)

![Screenshot 2](img/ss2.gif)

VimModelines adds [Vim](http://www.vim.org/) modeline support into
[Sublime Text 3](https://www.sublimetext.com/) for common settings. Modelines
are Vim commands embedded into the comments in headers or footers. They are
commonly used to set attributes specific to the file, like indentation or line
endings to override the editor's default settings.

They are the Vi/Vim equivalent of [Emacs](https://www.gnu.org/software/emacs/)
modelines.

Their inclusion into files like `Makefile`, which must be tab delimited, or in
projects with many contributors is common-ish. They are also a common mechanism
to [define the source encoding](https://www.python.org/dev/peps/pep-0263/#defining-the-encoding)
for Python 2.

This plugin, by default, will search for them on file load & save and apply them
to the Sublime Text view.

The default settings file for this plugin, for example, uses tabs and has
preference for a width of 2. This will override your default settings if
`apply_on_load` is set to `true`.

![Screenshot 1](img/ss1.png)

## Parsed Attributes

| Attribute          | Description                               | Mapping     |
| ------------------ | ----------------------------------------- | ----------- |
| autoindent, ai     | Automatic indentation           | `auto_indent = True`  |
| noautoindent, noai | Disable automatic indentation   | `auto_indent = False` |
| fileformat, ff     | Set line endings (dos, mac, unix) | `set_line_endings()` |
| tabstop, ts        | # of columns for each tab character       | `tab_size`  |
| shiftwidth, sw     | # of columns for indent operation         | **ignored** |
| softtab, st        | # of columns for tab key (space & tab)    | **ignored** |
| expandtab, et      | Tabs → Spaces      | `translate_tabs_to_spaces = True`  |
| noexpandtab, noet  | Respect tab chars  | `translate_tabs_to_spaces = False` |
| number, nu         | Show line numbers              | `line_numbers = True`  |
| nonumber, nonu     | Hide line numbers              | `line_numbers = False` |
| wrap               | Enable word wrap                  | `word_wrap = True`  |
| nowrap             | Disable word wrap                 | `word_wrap = False` |

## Requirements

- [Sublime Text 3](https://www.sublimetext.com/)

## Installation Instructions

### Using Package Control

1. [Install Package Control](https://packagecontrol.io/installation)
2. Open the Command Palette (⌘+⇧+P on macOS or ⌃+⇧+P on Linux & Windows)
2. Search for and select "Package Control: Install Package"
3. Search for and install "VimModelines"

### Manually

1. `cd` into your "Packages" directory:

| Platform |                                                          |
| -------- | -------------------------------------------------------- |
| Linux    | `~/.config/sublime-text-3/Packages/`                     |
|  macOS  | `~/Library/Application Support/Sublime Text 3/Packages/` |
| Windows  | `%APPDATA%\Sublime Text 3\Packages\`                     |

2. Clone the repository:

```bash
git clone https://github.com/pestilence669/VimModelines.git
```
