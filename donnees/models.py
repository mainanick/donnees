from collections import namedtuple

from donnees.db import Query, QueryResult


class Model(Query):
    table_name = None
    fields = None
    related = None    

    @classmethod
    def get(cls, **kwargs):
        results, sql = cls.select(
            table=cls.table_name, columns=cls.fields, **kwargs)        
        return cls.build_response(results, sql)

    @classmethod
    def query(cls, sql):
        result, sql = cls.raw_query(sql)        
        return cls.build_response(result, sql, raw_query=True)

    @classmethod
    def build_response(cls, results, sql, raw_query=False):
        if cls.fields is None and not raw_query:            
            return QueryResult(results, sql)
        
        if not raw_query:
            response_tuple = namedtuple(cls.__name__, cls.fields)
            _response = [r for r in map(response_tuple._make, results)]
            return QueryResult(_response, sql)

        #TODO get the table columns from db
        return QueryResult(results, sql)
