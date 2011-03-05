Journal
=======

A simple, private day-to-day journal web app written in Python.

Journal entries are stored in plain text files where the filename reflects
the date of entry (as a UNIX timestamp). Newlines in posts are converted
to HMTL line breaks on rendering, but no other markup is rendered.

Password access is required to view or post any entry. It is advised to
set the permissions on the entries/ directory to something suitably
strict if you wish to keep entries private.

To set up, clone the source and then copy sample__config.py and
sample__password.py to config.py and password.py and edit them as
appropriate. password.py should contain the SHA256 sum of the desired
password, as might be generated as:
  $ echo -n "password" | sha256sum

No facility for editing or deleting journal entries is provided, though you
could always edit the text files themselves.

Written by Adam Greig in March 2011.
All code released into the public domain.

