import pandas as pd
from donnees.db import DatabaseConnection


class QueryResult(object):
    _sql = None
    _results = None

    def __init__(self, results, sql):
        self._sql = sql
        self._results = results

    def __getitem__(self, key):
        if self.results:
            return self._results[key]
        raise ValueError("QuerySet Item not found")

    def __iter__(self):
        return iter(self._results)

    def __str__(self):
        return "<QueryResult [{}]>".format(len(self._results))

    @property
    def sql(self):
        """Return the last run sql statement"""
        return self._sql

    @property
    def df(self):
        """Returns a Pandas DataFrame instance"""
        dataframe = pd.DataFrame.from_records(self._results)
        return dataframe

    @property
    def results(self):
        yield self._results


class Query(object):
    db = DatabaseConnection()

    @classmethod
    def raw_query(self, sql):
        return self.db.execute(sql), sql

    @classmethod
    def select(self, table, columns, **kwargs):
        sql = "SELECT {columns} FROM {table_name}"
        _columns = ", ".join([c for c in columns]) if columns is not None else "*"
        sql = sql.format(columns=_columns, table_name=table)

        # Add where clause
        if kwargs:
            where = ["{}='{}'".format(field, value) for field, value in kwargs.items()]
            sql_where = " AND ".join([w for w in where])
            
            sql = "{sql} WHERE {where}".format(sql=sql, where=sql_where)


        return self.db.execute(sql), sql
