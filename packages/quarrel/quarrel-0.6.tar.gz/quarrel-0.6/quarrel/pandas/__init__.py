from .. import cooked
from ..templates import load_sql
from concentric.managers import Alchemist


def query(
        using,
        filename_or_sql,
        params=None,
        context=None,
        use_cache=True,
        select=True):
    """
    Executes a query and returns the results from fetchall
    as a dataframe

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
    from pandas import DataFrame
    return DataFrame(cooked.query(
        using, filename_or_sql, params, context,
        use_cache, select))


def query_alchemy(
        using,
        filename_or_sql,
        params=None,
        context=None, **kwargs):
    """
    Executes a query and returns the results from fetchall
    as a dataframe

    :param str using: the concentric alias for this connection
    :param str filename_or_sql: the /path/to/filename to render as a template,
        or the sql query that we want to execute
    :param list params: the list of parameters to use, the placeholders
        in the string will be connection-specific, e.g., `:` style parameters
        for oracle and `?` style parameters for mysql and mssql
    :param dict context: the context that will be used when rendering
        the template
    """
    import pandas
    sql = load_sql(using, filename_or_sql, context)
    with Alchemist.read_only(using) as session:
        return pandas.read_sql_query(sql, session.bind, params=params, **kwargs)

