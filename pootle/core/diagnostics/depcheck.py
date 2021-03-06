from django.conf import settings
from . import checks


def required_checks():
    # TODO move the other checks to this system
    dependencies = []
    for app in settings.INSTALLED_APPS:
        if app.startswith("django"):
            # XXX ideally, we check for app.startswith("pootle.")
            # but we are not there yet.
            continue
        try:
            module = __import__(app + ".dependencies")
        except ImportError:
            continue
        dependencies += module.test_dependencies()

    return dependencies


def optional_checks():
    optional = []

    if not checks.test_unzip():
        optional.append({
            "dependency": "unzip",
            "text": _("Can't find the unzip command. Uploading archives is "
                      'faster if "unzip" is available.')
        })
    if not checks.test_iso_codes():
        optional.append({
            "dependency": "iso-codes",
            "text": _("Can't find the ISO codes package. Pootle uses ISO codes"
                      " to translate language names.")
        })
    if not checks.test_levenshtein():
        optional.append({
            "dependency": "levenshtein",
            "text": _("Can't find python-levenshtein package. Updating against"
                      " templates is faster with python-levenshtein.")
        })
    if not checks.test_indexer():
        optional.append({
            "dependency": "indexer",
            "text": _("No text indexing engine found. Searching is faster if "
                      "an indexing engine like Xapian or Lucene is installed.")
        })
    if not checks.test_chardet():
        optional.append({
            "dependency": "chardet",
            "text": _("Can't find chardet package. Automatic detection of"
                      "encodings may be faulty.")
        })

    filter_name, filter_args = get_markup_filter()
    if filter_name is None:
        text = None
        if filter_args == "missing":
            text = _("MARKUP_FILTER is missing. Falling back to HTML.")
        elif filter_args == "misconfigured":
            text = _("MARKUP_FILTER is misconfigured. Falling back to HTML.")
        elif filter_args == "uninstalled":
            text = _("Can't find the package which provides %r markup support. "
                     "Falling back to HTML.",
                     settings.MARKUP_FILTER[0])
        elif filter_args == "invalid":
            text = _("Invalid value %r in MARKUP_FILTER. Falling back to "
                     "HTML.", settings.MARKUP_FILTER[0])

        if text is not None:
            optional.append({
                "dependency": filter_args + "-markup",
                "text": text
            })

    return optional


def optimal_checks():
    optimal = []

    if not checks.test_db():
        if checks.test_mysqldb():
            text = _("Using the default sqlite3 database engine. SQLite is "
                     "only suitable for small installations with a small "
                     "number of users. Pootle will perform better with the "
                     "MySQL database engine.")
        else:
            text = _("Using the default sqlite3 database engine. SQLite is "
                     "only suitable for small installations with a small "
                     "number of users. Pootle will perform better with the "
                     "MySQL database engine, but you need to install "
                     "python-MySQLdb first.")
        optimal.append({"dependency": "db", "text": text})

    if checks.test_cache():
        if checks.test_memcache():
            if not checks.test_memcached():
                # memcached configured but connection failing
                optimal.append({
                    "dependency": "cache",
                    "text": _("Pootle is configured to use memcached as a "
                              "caching backend, but can't connect to the "
                              "memcached server. Caching is currently "
                              "disabled.")
                })
            else:
                if not checks.test_session():
                    text = _("For optimal performance, use django.contrib."
                             "sessions.backends.cached_db as the session "
                             "engine.")
                    optimal.append({"dependency": "session", "text": text})
        else:
            optimal.append({
                "dependency": "cache",
                "text": _("Pootle is configured to use memcached as caching "
                          "backend, but Python support for memcached is not "
                          "installed. Caching is currently disabled.")
            })
    else:
        optimal.append({
            "dependency": "cache",
            "text": _("For optimal performance, use memcached as the caching "
                      "backend.")
        })

    if not checks.test_webserver():
        optimal.append({
            "dependency": "webserver",
            "text": _("For optimal performance, use Apache as the webserver.")
        })
    if not checks.test_from_email():
        optimal.append({
            "dependency": "from_email",
            "text": _('The "from" address used to send registration emails is '
                      "not specified. Also review the mail server settings.")
        })
    if not checks.test_contact_email():
        optimal.append({
            "dependency": "contact_email",
            "text": _("No contact address is specified. The contact form will "
                      "allow users to contact the server administrators.")
        })
    if not checks.test_debug():
        optimal.append({
            "dependency": "debug",
            "text": _("Running in debug mode. Debug mode is only needed when "
                      "developing Pootle. For optimal performance, disable "
                      "debugging mode.")
        })

    return optimal
