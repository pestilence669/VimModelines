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
        self.apply_on_live_edits = self.settings.get('apply_on_live_edits')
        self.apply_on_load = self.settings.get('apply_on_live_edits')

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command('close_file')

        # restore old settings
        self.settings.set('apply_on_load', self.apply_on_load)
        self.settings.set('apply_on_live_edits', self.apply_on_live_edits)
        self.settings.get('line_count', self.line_count)

    def setText(self, string):
        self.view.run_command('select_all')
        self.view.run_command('right_delete')
        self.view.run_command('insert', {'characters': string})

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def toggle_helper(self, true_flags, false_flags, variable):
        '''Tests vim flags effects on settings to a given ST variable'''

        def condition_set():
            return self.view.settings().get(variable)

        def condition_unset():
            return not condition_set()

        for (true_flag, false_flag) in zip(true_flags, false_flags):
            self.setText('# vim: set {}:'.format(true_flag))
            yield condition_set()
            self.assertTrue(condition_set())

            self.setText('# vim: set {}:'.format(false_flag))
            yield condition_unset()
            self.assertTrue(condition_unset())

    ###########################################################################

    def test_initial_settings_are_sane(self):
        '''Ensure tab_size isn't suggestively invalid at 19 or 79'''
        self.assertNotEqual(19, self.view.settings().get('tab_size'))
        self.assertNotEqual(79, self.view.settings().get('tab_size'))

    def test_setting_tab_size1(self):
        self.settings.set('apply_on_live_edits', True)

        def condition():
            return 19 == self.view.settings().get('tab_size')

        self.setText('# vim: set ts=19:')
        yield condition
        self.assertTrue(condition())

    def test_setting_tab_size2(self):
        self.settings.set('apply_on_live_edits', True)

        def condition():
            return 19 == self.view.settings().get('tab_size')

        self.setText('# vim: set tabstop=19:')
        yield condition
        self.assertTrue(condition())

    def test_setting_tab_size_with_cascade(self):
        self.settings.set('apply_on_live_edits', True)

        def condition():
            return 79 == self.view.settings().get('tab_size')

        self.setText('# vim: set ts=19:\n# vim: set ts=79:')
        yield condition
        self.assertTrue(condition())

    def test_setting_line_endings(self):
        self.settings.set('apply_on_live_edits', True)

        cases = (('ff', 'mac', 'cr'),
                 ('ff', 'dos', 'windows'),
                 ('ff', 'unix', 'unix'),
                 ('fileformat', 'mac', 'cr'),
                 ('fileformat', 'dos', 'windows'),
                 ('fileformat', 'unix', 'unix'))

        for (attr, value, expected_sublime_value) in cases:
            condition = lambda: expected_sublime_value == \
                                self.view.line_endings().lower()

            self.setText('# vim: set {}={}:'.format(attr, value))
            yield condition
            self.assertTrue(condition())

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

        def condition():
            return 19 == self.view.settings().get('tab_size')

        yield condition
        self.assertTrue(condition())

    def test_header_at_edge_of_bounds(self):
        self.settings.set('apply_on_live_edits', True)

        lines = ['Line #{}\n'.format(i)
                 for i in range(1, self.line_count)]
        lines.append('# vim: set ts=19:')

        def condition():
            return 19 == self.view.settings().get('tab_size')

        self.setText(''.join(lines))
        yield condition
        self.assertEqual(19, self.view.settings().get('tab_size'))

    def test_footer_at_end_of_bounds(self):
        self.settings.set('apply_on_live_edits', True)

        lines = ['Line #{}\n'.format(i)
                 for i in range(1, self.line_count * 3)]
        lines.append('# vim: set ts=19:')

        def condition():
            return 19 == self.view.settings().get('tab_size')

        self.setText(''.join(lines))
        yield condition
        self.assertTrue(condition())

    def test_footer_at_edge_of_bounds(self):
        self.settings.set('apply_on_live_edits', True)

        lines = ['Line #{}'.format(i)
                 for i in range(1, self.line_count * 2)]

        lines.append('# vim: set ts=19:')

        lines.extend('Line #{}'.format(i)
                     for i in range(self.line_count * 2 + 1,
                                    self.line_count * 3))

        def condition():
            return 19 == self.view.settings().get('tab_size')

        self.setText('\n'.join(lines))
        yield condition
        self.assertTrue(condition())

    # def test_footer_out_of_bounds(self):
    #     self.settings.set('apply_on_live_edits', True)

    #     lines = ['Line #{}'.format(i)
    #              for i in range(1, self.line_count * 2)]

    #     lines.append('# vim: set ts=19:')

    #     lines.extend('Line #{}'.format(i)
    #                  for i in range(self.line_count * 2 + 1,
    #                                 self.line_count * 3 + 1))

    #     current_tab_size = self.view.settings().get('tab_size')

    #     def condition():
    #         return 19 == self.view.settings().get('tab_size')

    #     self.setText('\n'.join(lines))
    #     yield 6000
    #     yield condition
    #     self.assertTrue(condition())

    # def test_header_out_of_bounds(self):
    #     self.settings.set('apply_on_live_edits', True)

    #     lines = ['Line #{}\n'.format(i)
    #              for i in range(1, self.line_count + 1)]
    #     lines.append('vim: set ts=19')

    #     current_tab_size = self.view.settings().get('tab_size')

    #     def condition():
    #         return 19 == self.view.settings().get('tab_size')

    #     # this needs to timeout, as we don't want a change to occur
    #     self.setText(''.join(lines))
    #     yield condition
    #     self.assertTrue(condition())
