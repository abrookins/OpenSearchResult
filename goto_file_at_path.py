import re
import os
import sublime, sublime_plugin


# Matches lines of the format: "102: <some text here>"
LINE_NUMBER_RE = '^\s*[0-9]*:'


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

        if view.name() != 'Find Results':
            return

        for s in view.sel():
            line = view.line(s)
            line_str = view.substr(view.line(s))
            line_is_result = re.search(LINE_NUMBER_RE, line_str)

            if line_str.startswith('/') or line_str.endswith(':') \
                or line_is_result:
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


class OpenSearchResultCommand(sublime_plugin.TextCommand):
    """
    Open a file listed in the Find In File search results at the line the
    cursor is on, or just open the file if the cursor is on the file path.
    """

    def open_file_from_line(self, line, line_num):
        """
        Attempt to parse a file path from the string `line` and open it in a
        new buffer.
        """
        if ':' not in line:
            return

        file_path = line.split(':')[0]

        if os.path.exists(file_path):
            self.view.window().open_file(
                "%s:%s" % (file_path, line_num), sublime.ENCODED_POSITION)

    def previous_line(self, region):
        """ `region` should be a Region covering the entire hard line """
        if region.begin() == 0:
            return None
        else:
            return self.view.full_line(region.begin() - 1)

    def run(self, edit):
        for cursor in self.view.sel():
            cur_line = self.view.line(cursor)
            line_str = self.view.substr(cur_line).strip()

            if self.view.name() != 'Find Results':
                return

            # Only a search result matching the find will include a colon.
            line_is_search_result = re.search(LINE_NUMBER_RE, line_str)

            if line_str.startswith('/') and line_str.endswith(':'):
                file_path = line_str.split(':')[0]
                if os.path.exists(file_path):
                    self.view.window().open_file(file_path)
            elif line_is_search_result:
                # In a line of the format "<line_num>: <text>" this grabs line_num.
                line_num = line_str.strip().split(':')[0]

                # Count backwards until we find a path or the beginning of the file.
                prev = cur_line
                while True:
                    prev = self.previous_line(prev)
                    if prev == None:
                        break

                    line = self.view.substr(prev).strip()
                    if line.startswith('/') and line.endswith(':'):
                        return self.open_file_from_line(line, line_num)
