import os
import sublime, sublime_plugin


class HighlightFilePaths(sublime_plugin.EventListener):
    HIGHLIGHT_REGION_NAME = 'HighlightFilePaths'
    SCOPE_SETTINGS_KEY = 'highlight_file_scope'
    ICON_SETTINGS_KEY = 'highlight_file_icon'
    DEFAULT_SCOPE = 'highlight_file_path'
    DEFAULT_ICON = ''

    def show_highlight(self, view):
        valid_regions = []
        scope = view.settings().get(self.SCOPE_SETTINGS_KEY, self.DEFAULT_SCOPE)
        icon = view.settings().get(self.ICON_SETTINGS_KEY, self.DEFAULT_ICON)

        for s in view.sel():
            line = view.line(s)
            line_str = view.substr(view.line(s))
            if not line_str.startswith('/') or not line_str.endswith(':'):
                continue
            valid_regions.append(line)

        if valid_regions:
            view.add_regions(
                self.HIGHLIGHT_REGION_NAME, valid_regions, 
                scope, icon, sublime.DRAW_EMPTY | sublime.DRAW_OUTLINED)
        else:
            view.erase_regions(self.HIGHLIGHT_REGION_NAME)

    def on_selection_modified(self, view):
        if view.settings().get('is_widget') \
            or not view.settings().get('highlight_file_paths') \
            or not view.settings().get('command_mode'):
            view.erase_regions(self.HIGHLIGHT_REGION_NAME)
            return
        self.show_highlight(view)

    def on_deactivated(self, view):
        view.erase_regions(self.HIGHLIGHT_REGION_NAME)

    def on_activated(self, view):
        if view.settings().get('highlight_file_paths'):
            self.show_highlight(view)


class GotoFileAtPathCommand(sublime_plugin.TextCommand):
    """ Open files listed in the Find in File results buffer. """

    def run(self, edit):
        """
        If the user runs this command while on a line that starts with '/' and
        ends with ':', open the file.
        """
        cursor = self.view.sel()[0]
        line = self.view.substr(self.view.line(cursor))

        if line.startswith('/') and line.endswith(':'):
            file_path = line.split(':')[0]
            if os.path.exists(file_path):
                self.view.window().open_file(file_path)