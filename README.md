# `mp3-split` README

`mp3-split` is a command-line utility that splits a long MP3 file into smaller
files and then tags them with the track name and track number.

# Development

-   Python 3.7+
-   PyYAML
-   python-ffmpeg

`ffmpeg` is an external dependency and needs to be present on your path.

# Usage

Usage: `mp3-split` `INPUT_FILE` `CONFIG_FILE`

Example `CONFIG_FILE` layout:

```yaml
artist: "A band"
title: "An album"
tracks:
  - name: Track Name 1
    offset: "0:00"
  - name: The Second Track
    offset: "3:26"
  - name: A Third Piece
    offset: "26:01"
```

Files will be created in `[ARTIST]/[ALBUM]/`, which will be created if it does
not exist.

Setting the `LOGLEVEL=DEBUG` environment variable will show debug output.

# Improvements

-   Converted to use Poetry, making the script installable.
-   Included the track number in the filename.
-   Removed the need for subprocess shells.
-   Removed dependencies on eyeD3 and mp3info, handling these using the Python
    ffmpeg bindings instead.
-   Significant code cleanup including a ~50% length reduction.
-   Added doc strings to all functions.
-   Added a VSCode devcontainer configuration for easier dependency management.
-   Added pre-commit checks.
-   Converted the config file to YAML, enabling easier parsing and adding more
    optional tags, starting with artist and album name.
-   Quietened output by default, using the logging module to specify log level.
-   Converted to use Click for CLI handling, simplifying argument parsing and
    file access.
-   Removed a lot of unnecessary re-computing of information already in the
    config file; only the total length needs to be computed.

# TODO

-   Remove the external dependency on the ffmpeg binary.
-   Add tests.

# Credits

-   Original author: Daniel Teichman <https://github.com/danielteichman>
-   Significant rewrite by Chris Cunningham <https://github.com/thumperward>
