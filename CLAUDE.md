# Notes for Claude

## Change log (required for every new version)

Every time a new app version ships (VERSION_NUM in `app-prototype/index.html` goes up), log it:

1. Append one row per change to `changelog/changes.csv`, newest at the bottom. Columns:
   Version, Date (UTC), Change, Requested by, Area / Page, Type (Feature, Fix, Design or Data),
   On public site (Y/N), Status (usually Current), Notes.
2. Run `python3 changelog/build_changelog.py` to rebuild `changelog/change-log.xlsx`.
3. If a change undoes or alters an earlier row, update that row's Status (for example "Removed in v115").
4. Commit the CSV and the rebuilt spreadsheet with the version itself.

The project's shared folder (`changelog/`) holds the master copy; keep the two in step.
Never edit `change-log.xlsx` by hand, since the build script overwrites it.
