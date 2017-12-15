#!/usr/bin/env python
# vim: set ts=4 sw=4 et fileencoding=utf-8:

from os import path
from unittesting import DeferrableTestCase
import sublime


version = sublime.version()


class TestVimModelines(DeferrableTestCase):
    '''Exercises the VimModelines plugin to check for expected use.'''

    SETTINGS_FILE = 'VimModelines.sublime-settings'

    def setUp(self):
        self.view = sublime.active_window().new_file()
        # make sure we have a window to work with
        s = sublime.load_settings('Preferences.sublime-settings')
        s.set('close_windows_when_empty', False)

        # save current settings
        self.settings = sublime.load_settings(self.SETTINGS_FILE)
        self.line_count = self.settings.get('line_count')
        self.apply_on_load = self.settings.get('apply_on_load')
        self.apply_on_save = self.settings.get('apply_on_save')

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command('close_file')

        # restore old settings
        self.settings.set('apply_on_save', self.apply_on_save)
        self.settings.set('apply_on_load', self.apply_on_load)
        self.settings.get('line_count', self.line_count)

    def setText(self, string):
        self.view.run_command('select_all')
        self.view.run_command('right_delete')
        self.view.run_command('insert', {'characters': string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def toggle_helper(self, true_flags, false_flags, variable):
        '''Tests vim flags effects on settings to a given ST variable'''

        def variable_set():
            return self.view.settings().get(variable)

        for (true_flag, false_flag) in zip(true_flags, false_flags):
            self.setText('# vim: set {}:'.format(true_flag))
            self.apply()
            self.assertTrue(variable_set())

            self.setText('# vim: set {}:'.format(false_flag))
            self.apply()
            self.assertTrue(not variable_set())

    def apply(self):
        self.view.window().run_command('vim_modelines_apply')

    ###########################################################################

    def test_initial_view_settings_are_sane(self):
        '''Ensure tab_size isn't suggestively invalid at 19 or 79'''
        self.assertNotEqual(19, self.view.settings().get('tab_size'))
        self.assertNotEqual(79, self.view.settings().get('tab_size'))

    def test_default_plugin_settings(self):
        '''Ensure that the defaults are read from the config'''
        self.assertTrue(self.view.settings().get('apply_on_load'))
        self.assertTrue(self.view.settings().get('apply_on_save'))
        self.assertEqual(5, self.view.settings().get('line_count'))

    def test_setting_tab_size(self):
        self.setText('# vim: set ts=19:')
        self.apply()
        self.assertEqual(19, self.view.settings().get('tab_size'))

    def test_setting_tab_size_with_cascade(self):
        self.setText('# vim: set ts=19:\n# vim: set ts=79:')
        self.apply()
        self.assertEqual(79, self.view.settings().get('tab_size'))

    def test_setting_line_endings(self):
        cases = (('ff', 'mac', 'cr'),
                 ('ff', 'dos', 'windows'),
                 ('ff', 'unix', 'unix'),
                 ('fileformat', 'mac', 'cr'),
                 ('fileformat', 'dos', 'windows'),
                 ('fileformat', 'unix', 'unix'))

        for (attr, value, expected_sublime_value) in cases:
            self.setText('# vim: set {}={}:'.format(attr, value))
            self.apply()
            self.assertEqual(expected_sublime_value,
                             self.view.line_endings().lower())

    def test_setting_and_unsetting_line_numbers(self):
        self.toggle_helper(['number', 'nu'],
                           ['nonumber', 'nonu'],
                           'line_numbers')

    def test_setting_and_unsetting_word_wrap(self):
        self.setText('really long line' * 500)
        self.toggle_helper(['wrap'],
                           ['nowrap'],
                           'word_wrap')

    def test_setting_and_unsetting_auto_indent(self):
        self.toggle_helper(['autoindent', 'ai'],
                           ['noautoindent', 'noai'],
                           'auto_indent')

    def test_setting_and_unsetting_translate_tabs_to_spaces(self):
        self.toggle_helper(['expandtab', 'et'],
                           ['noexpandtab', 'noet'],
                           'translate_tabs_to_spaces')

    def test_apply_on_load(self):
        self.settings.set('apply_on_load', True)

        self.view.set_scratch(True)
        self.view.window().focus_view(self.view)
        self.view.window().run_command('close_file')

        f = path.join(path.dirname(__file__), 'assets', 'open_file_test.txt')
        self.view = sublime.active_window().open_file(f)
        yield lambda: not self.view.is_loading()

        self.apply()
        self.assertEqual(19, self.view.settings().get('tab_size'))

    def test_header_at_edge_of_bounds(self):
        lines = ['Line #{}\n'.format(i)
                 for i in range(1, self.line_count)]
        lines.append('# vim: set ts=19:')

        self.setText(''.join(lines))
        self.apply()
        self.assertEqual(19, self.view.settings().get('tab_size'))

    def test_footer_at_end_of_bounds(self):
        lines = ['Line #{}\n'.format(i)
                 for i in range(1, self.line_count * 3)]
        lines.append('# vim: set ts=19:')

        self.setText(''.join(lines))
        self.apply()
        self.assertEqual(19, self.view.settings().get('tab_size'))

    def test_footer_at_edge_of_bounds(self):
        lines = ['Line #{}'.format(i)
                 for i in range(1, self.line_count * 2)]

        lines.append('# vim: set ts=19:')

        lines.extend('Line #{}'.format(i)
                     for i in range(self.line_count * 2 + 1,
                                    self.line_count * 3))

        self.setText('\n'.join(lines))
        self.apply()
        self.assertEqual(19, self.view.settings().get('tab_size'))

    def test_footer_out_of_bounds(self):
        lines = ['Line #{}'.format(i)
                 for i in range(1, self.line_count * 2)]
        lines.append('# vim: set ts=19:')
        lines.extend('Line #{}'.format(i)
                     for i in range(self.line_count * 2 + 1,
                                    self.line_count * 3 + 1))

        current_tab_size = self.view.settings().get('tab_size')

        self.setText('\n'.join(lines))
        self.apply()
        self.assertNotEqual(19, self.view.settings().get('tab_size'))

    def test_header_out_of_bounds(self):
        lines = ['Line #{}'.format(i)
                 for i in range(1, self.line_count + 1)]
        lines.append('vim: set ts=19')
        lines.extend('Line #{}'.format(i)
                     for i in range(self.line_count + 2,
                                    self.line_count * 3 + 1))

        current_tab_size = self.view.settings().get('tab_size')

        self.setText('\n'.join(lines))
        self.apply()
        self.assertNotEqual(19, self.view.settings().get('tab_size'))
