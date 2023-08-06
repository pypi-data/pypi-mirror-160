from ..connections import get_connection
from ..raw import open_cursor


def query(
        using,
        filename_or_sql,
        params=None,
        context=None,
        use_cache=True,
        select=True):
    """
    Executes a query and returns the results from fetchall
    as a list of dicts. the keys of each dictionary will all be
    lowercased.

    :param str using: the concentric alias for this connection
    :param str filename_or_sql: the /path/to/filename to render as a template,
        or the sql query that we want to execute
    :param list params: the list of parameters to use, the placeholders
        in the string will be connection-specific, e.g., `:` style parameters
        for oracle and `?` style parameters for mysql and mssql
    :param dict context: the context that will be used when rendering
        the template
    :param bool use_cache: if True, we will try to use / reuse a cached connection
        otherwise, we will pull a fresh connection
    :param bool select: if the query that we are running expects results returned
    """
    close, conn = get_connection(using, use_cache)
    cursor = None
    try:
        cursor = open_cursor(
            using, conn, filename_or_sql, params, context, use_cache, select)
        if select:
            header = [ x[0].lower() for x in cursor.description ]
            data = [ dict(zip(header, x)) for x in cursor.fetchall() ]
            return data
    finally:
        cursor.close()
        if close and conn:
            conn.close()


def query_many(using, filename_or_sql, params=None, context=None, use_cache=True):
    """
    executes a query and then yields multiple results back.  This is useful
    for systems like sql server or vertica where a query can generate
    multiple result sets.
    """
    close, conn = get_connection(using)
    cursor = None
    try:
        cursor = open_cursor(
            using, conn, filename_or_sql,
            params, context, use_cache)
        done = False
        while not done:
            if cursor.description:
                header = [ x[0].lower().strip() for x in cursor.description ]
                data = []
                for x in cursor.fetchall():
                    data.append(dict(zip(header, x)))
                yield data
            done = not cursor.nextset()
    finally:
        if cursor:
            cursor.close()
        if close and conn:
            conn.close()


