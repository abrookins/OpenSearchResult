# Go to File at Path Plugin for Sublime Text 2

This plugin creates a command that allows you to open files listed in the search
results of the 'Find in Files' command.

As you move your cursor through the search results, any paths that are openable
will be highlighted in, by default, the "function" color of your color scheme.

If you run the command while the cursor is on a line that is openable, the file
will open in a new tab.

## Key Binding

The default key binding is a Vintage command mode key: "go".

## Customizing

You can change various things about the plugin by adding user settings:

- 'highlight_file_paths': Set to false to disable highlighting openable paths (the command will still work)
- 'highlight_file_scope': The scope that will be used to color the outline for
openable paths. See your theme file for examples.
- 'highlight_file_icon': If you want an icon to show up in the gutter next to
openable paths, include a valid icon name as a string (e.g., 'circle', 'dot')
(see Sublime Text 2 API docs for View.add_regions() for valid icon names)
