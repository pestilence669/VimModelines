# vim: set ts=4 sw=4 et fileencoding=utf-8:
'''Parse and apply Vim modelines

GitHub: https://github.com/pestilence669/VimModelines
License: MIT
'''

from __future__ import print_function
import sublime
import sublime_plugin
import os
import re
import sys


PLUGIN_NAME = 'VimModelines'
SETTINGS_FILE = 'VimModelines.sublime-settings'


def plugin_loaded():
    print('Loaded {}'.format(PLUGIN_NAME))

    # to handle the async loading of plugins
    _mod = sys.modules[__name__]
    listener = _mod.plugins[0]
    for w in sublime.windows():
        for g in range(w.num_groups()):
            listener.on_load(w.active_view_in_group(g))


def plugin_unloaded():
    print('Unloaded {}'.format(PLUGIN_NAME))


class VimModelines(sublime_plugin.EventListener):
    '''Plugin entry point'''

    def __init__(self):
        self.modeline_RX = re.compile('vim(?:\d*):\s*(?:set)?\s*(.*)$')
        self.attr_sep_RX = re.compile('[: ]')
        self.attr_kvp_RX = re.compile('([^=]+)=?([^=]*)')

        self.__settings = None

    @property
    def settings(self):
        '''plugin settings, lazy loading for API readiness'''
        if self.__settings is None:
            self.__settings = sublime.load_settings(SETTINGS_FILE)
        return self.__settings

    def description(self):
        return __doc__.split('\n')[0]

    def on_load(self, view):
        if self.settings.get('apply_on_load', False):
            self.apply_modelines(view)

    def on_post_save(self, view):
        if self.settings.get('apply_on_save', False):
            self.apply_modelines(view)

    def on_modified_async(self, view):
        if self.settings.get('apply_on_live_edits', False):
            self.apply_modelines(view, live=True)

    ###########################################################################

    def apply_modelines(self, view, live=False):
        if view.is_scratch():
            return

        attrs = filter(None.__ne__, map(self.parse_for_modeline,
                                        self.get_header_and_footer(view,
                                                                   live)))

        for line in attrs:
            for attr, value in line:
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

    def get_header_and_footer(self, view, live=False):
        line_count = self.settings.get('line_count', 0)

        lines = []

        if not line_count:
            return lines

        # add +1, because the intersection test in non-inclusive
        header_region = sublime.Region(0, view.text_point(line_count, 0) + 1)

        max_line = view.rowcol(view.size())[0] + 1
        ftr_line = max(line_count, max_line - line_count)
        if max_line - line_count > 0:
            footer_region = sublime.Region(view.text_point(ftr_line, 0),
                                           view.size() + 1)  # see above
        else:
            footer_region = None

        in_header = header_region and any(header_region.intersects(r)
                                          for r in view.selection)
        in_footer = footer_region and any(footer_region.intersects(r)
                                          for r in view.selection)

        if not live or in_header or in_footer:
            lines += view.lines(header_region)
            if footer_region:
                lines += view.lines(footer_region)

        return [view.substr(region) for region in lines]

    def parse_for_modeline(self, line):
        match = self.modeline_RX.search(line)

        if not match:
            return None
        else:
            modeline, = match.groups()
            attrs = [self.attr_kvp_RX.match(attr).groups()
                     for attr in filter(bool,
                                        self.attr_sep_RX.split(modeline))]

            return attrs
