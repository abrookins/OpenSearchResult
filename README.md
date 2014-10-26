# Open Search Result Plugin for Sublime Text 2

This plugin creates a command that allows you to open files listed in the search
results of the 'Find in Files' command.

- When run on a line in the search results that includes a line number, e.g., 
"102:    print 'foo'" it opens the file at the correct line number.

- When run on a line that contains a file path like '/path/to/somewhere:'
in the search listing, it opens the file without a line number specified.

## Key Binding

- The default key binding is a Vintage command mode key: "g, o".

## Customizing

You can change various things about the plugin by adding user settings:

- 'highlight_search_results': Set to false to disable highlighting openable
paths (the open command will still work)
- 'highlight_search_scope': The scope that will be used to color the outline for
openable paths or the icon. See your theme file for examples of colors.
- 'highlight_search_icon': If you want an icon to show up in the gutter next to
openable paths, include a valid icon name as a string (e.g., 'circle', 'dot' or
'bookmark')
- 'open_search_result_everywhere': Set to true to enable this plugin on all
files not just Find Results panes. You can use this for saving and reopening
your find results.

## Installing

### With Package Control

The easiest way to install Open Search Result is via the [Package Control](http://wbond.net/sublime_packages/package_control) for Sublime Text.

Once you install Package Control, restart Sublime Text and bring up the Command Palette with <kbd>Command</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> on OS X or <kbd>Control</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> on Linux/Windows.

Select "Package Control: Install Package", wait while Package Control fetches the latest package list, then select "OpenSearchResult" when the list appears. The advantage of using this method is that Package Control will automatically keep the package up-to-date.

### Without Package Control

Download this package, unzip it and put it in your Sublime Text Packages directory, which can usually be found at ` ~/Library/Application Support/Sublime Text 2/Packages/`.

Restart Sublime Text and you should be good to go.
