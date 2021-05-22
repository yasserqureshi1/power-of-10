
class QueryError(Exception):
    '''Exception raised when no results returned from query'''
    pass


class BroadQueryError(Exception):
    '''Exception raised when too many results are returned'''
    pass

