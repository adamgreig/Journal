Journal
=======

A simple, private day-to-day journal web app written in Python.

Journal entries are stored in plain text files where the filename reflects
the date of entry (as a UNIX timestamp). Newlines in posts are converted
to HMTL line breaks on rendering, but no other markup is rendered.

Password access is required to view or post any entry. It is advised to
set the permissions on the entries/ directory to something suitably
strict if you wish to keep entries private.

To set up, clone the source and then copy ``sample__config.py`` to
``config.py``, editing the secret key and password. The password is
the SHA256 sum of whatever you wish to use as a password, such as is
generated by:

``$ echo -n "password" | sha256sum``

Deployment is left as an exercise for the reader, though a development
server can be run by simply "python ./journal.py". For longer term uses,
Flask readily integrates with uWSGI and, say, the Cherokee web server.

No facility for editing or deleting journal entries is provided, though you
could always edit the text files themselves.

Written by Adam Greig in March 2011.
All code released into the public domain.
