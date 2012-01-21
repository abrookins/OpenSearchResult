import re
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


class OpenSearchResultCommand(sublime_plugin.TextCommand):
    """
    Open a file listed in the Find In File search results at the line the
    cursor is on.
    """

    def open_file_from_line(self, line):
        """
        Attempt to parse a file path from the string `line` and open it in a
        new buffer.
        """
        if ':' not in line:
            return

        file_path = line.split(':')[0]

        if os.path.exists(file_path):
            self.view.window().open_file(file_path)

    def previous_line(self, region):
        """ `region` should be a Region covering the entire hard line """
        if region.begin() == 0:
            return None
        else:
            return self.view.full_line(region.begin() - 1)

    def run(self, edit):
        cursor = self.view.sel()[0]
        cur_line = self.view.line(cursor)
        line_str = self.view.substr(cur_line).strip()

        # Only a search result matching the find will include a colon.
        # E.g., "102: <some text here>"
        line_is_result = re.search('^\s*[0-9]*:', line_str)

        if self.view.name() == 'Find Results' and line_is_result:
            # Count backwards until we find a path or the beginning of the file.
            prev = cur_line
            while True:
                prev = self.previous_line(prev)
                if prev == None:
                    break
                line = self.view.substr(prev).strip()
                if line.startswith('/') and line.endswith(':'):
                    return self.open_file_from_line(line)

