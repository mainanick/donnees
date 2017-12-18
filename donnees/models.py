from collections import namedtuple

from donnees.db import Query, QueryResult


class Model(Query):
    table_name = None
    fields = None
    related = None    

    @classmethod
    def get(cls, *args, **kwargs):
        results, sql = cls.select(
            table=cls.table_name, columns=cls.fields, **kwargs)        
        return cls.build_response(results, sql)

    @classmethod
    def query(cls, sql):
        result, sql = cls.raw_query(sql)        
        return cls.build_response(result, sql, with_fields=False)

    @classmethod
    def build_response(cls, results, sql, with_fields=True):
        if with_fields:
            response_tuple = namedtuple(cls.__name__, cls.fields)
            _response = [r for r in map(response_tuple._make, results)]
            return QueryResult(_response, sql)

        return QueryResult(results, sql)
