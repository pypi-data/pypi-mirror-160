import pmg

def connection_string_to_dict(connection_string: str) -> dict:
    return {kvp[0].upper(): kvp[1]
            for kvp in (kvp.split('=') for kvp in connection_string.split(';'))}

def execute(cn, sql, *args, **kwargs):
    cur = cn.cursor()
    cur.execute(sql, *args, **kwargs)
    return cur

def iter_cursor_as_dict(cur):
    columns = [column[0] for column in cur.description]
    for r in cur:
        yield dict(zip(columns, r))

def iter_cursor_as_namedtuple(cur):
    for r in iter_cursor_as_dict(cur):
        yield pmg.to_namedtuple(r)

def iter_cursor_sets(cur):
    "Iterate through all sets provided by a Python DB API 2.0 cursor"
    more = True
    if cur.description is not None:
        yield cur
    while more:
        more = cur.nextset()
        if cur.description is not None:
            yield cur

def iter_named_cursor_sets(cur):
    """Iterate through all named sets provided by a Python DB API 2.0 cursor.
    A set is named by the preceding set providing a single scalar called
    _DataTableName.
    """
    tab = None
    for rs in iter_cursor_sets(cur):
        if tab is None:
            assert len(rs.description) == 1 and \
                   rs.description[0][0] == '_DataTableName', \
                   'Every other result must be a scalar named _DataTableName.'
            tab = rs.fetchone()[0]
        else:
            yield (tab, rs)
            tab = None
