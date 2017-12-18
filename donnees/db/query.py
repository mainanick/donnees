# Copyright (c) 2017 Maina Nick

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

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
        import pandas

        dataframe = pandas.DataFrame.from_records(self._results)
        return dataframe

    @property
    def results(self):
        """Return the original result from db execute function"""
        return self._results


class Query(object):
    db = DatabaseConnection()

    @classmethod
    def raw_query(self, sql):
        """Execute a raw query"""
        return self.db.execute(sql), sql

    @classmethod
    def select(self, table, columns=None, **where):
        """Select data from a database
        params: table The table name
        params: columns The columns to be selected
        """
        sql = "SELECT {columns} FROM {table_name}"

        # select every column if column is not specified
        if columns is None:
            _columns = "*"
        else:
            _columns = ", ".join(["{}.{}".format(table, c) for c in columns])

        sql = sql.format(columns=_columns, table_name=table)

        # Add Where Fields
        if where:
            where_clauses = ["{}.{}='{}'".format(
                table, field, value) for field, value in where.items()]
            
            sql_where = " AND ".join([w for w in where_clauses])

            sql = "{sql} WHERE {where};".format(sql=sql, where=sql_where)

        return self.db.execute(sql), sql
