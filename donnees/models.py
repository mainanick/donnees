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
    def all(cls, **kwargs):
        return cls.get(**kwargs)

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

        # TODO get the table columns from db
        return QueryResult(results, sql)
