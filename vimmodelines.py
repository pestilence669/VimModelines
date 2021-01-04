# vim: set ts=4 sw=4 et fileencoding=utf-8:
'''Parse and apply Vim modelines

GitHub: https://github.com/pestilence669/VimModelines
'''

from itertools import chain
from .lib.encoding import ENCODING_MAP
import re
import sublime
import sublime_plugin


PLUGIN_NAME = 'VimModelines'
SETTINGS_FILE = 'VimModelines.sublime-settings'


def plugin_loaded():
    print('Loaded {}'.format(PLUGIN_NAME))

    # call on_load(), since files may load before the plugin (async)
    for w in sublime.windows():
        for g in range(w.num_groups()):
            VimModelines.instance.on_load(w.active_view_in_group(g))


def plugin_unloaded():
    print('Unloaded {}'.format(PLUGIN_NAME))


class Common():
    '''Shared functionality between plugins'''
    def __init__(self, *args):
        super().__init__(*args)
        self.__settings = None

    @property
    def settings(self):
        '''plugin settings, lazy loading for API readiness'''
        if self.__settings is None:
            self.__settings = sublime.load_settings(SETTINGS_FILE)
        return self.__settings


class VimModelines(Common, sublime_plugin.EventListener):
    '''Event listener to invoke the command on load & save'''

    instance = None  # last loaded instance (due to 3.1)

    def __init__(self, *args):
        super().__init__(*args)
        VimModelines.instance = self

    def on_load(self, view):
        if self.settings.get('apply_on_load', True):
            view.window().run_command('vim_modelines_apply')

    def on_post_save(self, view):
        if self.settings.get('apply_on_save', True):
            view.window().run_command('vim_modelines_apply')


###############################################################################

class VimModelinesCreateCommand(Common, sublime_plugin.TextCommand):
    '''Command containing the **create** main logic'''

    def run(self, edit):
        view = self.view
        if view.is_scratch():
            return

        settings = view.settings()
        ts = settings.get('tab_size')
        et = settings.get('translate_tabs_to_spaces')
        ai = settings.get('auto_indent')
        ff = view.line_endings()
        ww = settings.get('word_wrap')
        nu = settings.get('line_numbers')
        fe = view.encoding()

        _fe = None
        for vimenc, stenc in ENCODING_MAP.items():
            if fe == stenc:
                _fe = vimenc
                break

        if ff == 'windows':
            _ff = 'dos'
        elif ff == 'CR':
            _ff = 'mac'
        elif ff == 'Unix':
            _ff = 'unix'
        else:
            _ff = ff

        # vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
        ml = 'vim: set {}{} ts={} sts={} sw={} {} ff={} {} {} :'.format('enc=' + _fe + ' ' if _fe else '', 'et' if et else 'noet', ts, ts, ts, 'ai' if ai else 'noai', _ff, 'nu' if nu else 'nonu', 'wrap' if ww else 'nowrap')

        for region in view.sel():
            view.insert(edit, region.begin(), ml)


class VimModelinesApplyCommand(Common, sublime_plugin.WindowCommand):
    '''Command containing the **apply** main logic'''

    __modeline_RX = re.compile(r'''
        (?:^vim?                # begin line with either vi or vim
            | \s(?:vim? | ex))  # ... or whitespace then vi, vim, or ex
        (?:\d*):                # optional version digits, closed with :
        \s*                     # optional whitespace after ~vim700:
        (?:                     # alternation of type 1 & 2 modelines
            (?:set?[ ])([^ ].*):.*$ # type 2: optional set or se, spc, opts, :
            | (?!set?[ ])([^ ].*)$  # type 1: everything following
        )
    ''', re.VERBOSE)

    __attr_sep_RX = re.compile(r'[:\s]')
    __attr_kvp_RX = re.compile(r'([^=]+)=?([^=]*)')

    def run(self):
        view = self.window.active_view()
        if view.is_scratch():
            return

        view.erase_status(PLUGIN_NAME)
        line_count = self.settings.get('line_count', 5)

        # flatten each command or key/value pair and only keep the most recent
        attrs = dict(chain(*filter(None.__ne__,
                                   map(self.parse_for_modeline,
                                       self.header_and_footer(view,
                                                              line_count)))))

        for attr, value in attrs.items():
            if attr in ('tabstop', 'ts') and value.isdigit():
                view.settings().set('tab_size', int(value))
            elif attr in ('expandtab', 'et'):
                view.settings().set('translate_tabs_to_spaces', True)
            elif attr in ('noexpandtab', 'noet'):
                view.settings().set('translate_tabs_to_spaces', False)
            elif attr in ('autoindent', 'ai'):
                view.settings().set('auto_indent', True)
            elif attr in ('noautoindent', 'noai'):
                view.settings().set('auto_indent', False)
            elif attr in ('fileformat', 'ff'):
                if value == 'dos':
                    view.set_line_endings('windows')
                if value == 'unix':
                    view.set_line_endings('unix')
                if value == 'mac':
                    view.set_line_endings('CR')
            elif attr == 'wrap':
                view.settings().set('word_wrap', True)
            elif attr == 'nowrap':
                view.settings().set('word_wrap', False)
            elif attr in ('number', 'nu'):
                view.settings().set('line_numbers', True)
            elif attr in ('nonumber', 'nonu'):
                view.settings().set('line_numbers', False)
            elif attr in ('fenc', 'fileencoding'):
                target_encoding = ENCODING_MAP.get(value.lower())
                if not target_encoding:
                    view.set_status(PLUGIN_NAME,
                                    'Unsupported modeline encoding')
                else:
                    view.run_command('set_encoding',
                                     {'encoding': target_encoding})

    @staticmethod
    def header_and_footer(view, line_count):
        if not line_count:
            return []

        # header
        lines = view.lines(sublime.Region(0, view.text_point(line_count, 0)))

        # footer
        max_line = view.rowcol(view.size())[0] + 1
        ftr_line = max(line_count, max_line - line_count)
        if max_line - line_count > 0:
            lines += view.lines(sublime.Region(view.text_point(ftr_line, 0),
                                               view.size()))

        return map(view.substr, lines)

    @classmethod
    def parse_for_modeline(cls, line):
        '''Parse for each command or key/value pair if valid'''
        match = cls.__modeline_RX.search(line)

        if match:
            modeline = ''.join(m for m in match.groups() if m)
            attrs = [cls.__attr_kvp_RX.match(attr).groups()
                     for attr in filter(bool,
                                        cls.__attr_sep_RX.split(modeline))]

            return attrs
