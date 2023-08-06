from concentric.managers import Alchemist
from ..templates import load_sql


def query(using, filename_or_sql, params=None, context=None, select=True):
    sql = load_sql(using, filename_or_sql, context)
    fn = Alchemist.read_only
    if not select:
        fn = Alchemist.transactional
    with fn(using) as session:
        result = session.execute(sql, params)
        if select:
            keys = [ x.lower().strip() for x in result.keys() ]
            return [ dict(zip(keys, x)) for x in result.fetchall() ]
        return result
