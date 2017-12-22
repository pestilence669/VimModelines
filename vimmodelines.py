# vim: set ts=4 sw=4 et fileencoding=utf-8:
'''Parse and apply Vim modelines

GitHub: https://github.com/pestilence669/VimModelines
'''

from itertools import chain
from .lib.encoding import ENCODING_MAP
import re
import sublime
import sublime_plugin
import sys


PLUGIN_NAME = 'VimModelines'
SETTINGS_FILE = 'VimModelines.sublime-settings'


def plugin_loaded():
    print('Loaded {}'.format(PLUGIN_NAME))

    # call on_load(), since files will probably load before the plugin (async)
    listener = sys.modules[__name__].plugins[0]
    for w in sublime.windows():
        for g in range(w.num_groups()):
            listener.on_load(w.active_view_in_group(g))


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

    def on_load(self, view):
        if self.settings.get('apply_on_load', True):
            view.window().run_command('vim_modelines_apply')

    def on_post_save(self, view):
        if self.settings.get('apply_on_save', True):
            view.window().run_command('vim_modelines_apply')


###############################################################################


class VimModelinesApplyCommand(Common, sublime_plugin.WindowCommand):
    '''Command containing the main logic'''

    __modeline_RX = re.compile('vim(?:\d*):\s*(?:set)?\s*(.*)$')
    __attr_sep_RX = re.compile('[: ]')
    __attr_kvp_RX = re.compile('([^=]+)=?([^=]*)')

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
                    if view.encoding() != target_encoding:
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
            modeline, = match.groups()
            attrs = [cls.__attr_kvp_RX.match(attr).groups()
                     for attr in filter(bool,
                                        cls.__attr_sep_RX.split(modeline))]

            return attrs
