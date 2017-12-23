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

from donnees.utils import Attrvalue, format

JOIN = Attrvalue({'INNER': "INNER JOIN", 'OUTER': "OUTER JOIN"})


class QueryBuilder(object):
    def build(self):
        raise NotImplementedError


class Select(QueryBuilder):
    def __init__(self, table, columns="*", *clauses):
        self.columns = columns or "*"
        self.clauses = list(clauses)
        self.table = table

    def build(self):
        if self.columns != "*":
            x = ["{}.{}".format(self.table, c) for c in self.columns]
            self.columns = ", ".join(x)

        if not self.clauses:
            return "SELECT {} FROM {};".format(self.columns, self.table)

        _clauses = format(lambda clause: clause.build(), self.clauses)

        sql = " ".join(_clauses)
        built_sql = "SELECT {} FROM {} {};".format(
            self.columns, self.table, sql)

        return built_sql


class Join(QueryBuilder):
    """Example:
    INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID
    """

    def __init__(self, current_table, current_column, on_table,  on_column):
        self.current_table = current_table
        self.current_column = current_column
        self.on_table = on_table
        self.on_column = on_column

    def build(self):
        sql = JOIN.INNER + " {} ON {}.{} = {}.{}"
        return sql.format(self.on_table, self.current_table,
                          self.current_column, self.on_table, self.on_column)


class Order(QueryBuilder):
    def __init__(self, *columns):
        self.columns = columns

    @classmethod
    def get_order_type(cls, column):
        """Returns the formatted string and order type(either DESC or ASC) """
        if column[0] == '-':
            return "{} {}".format(column[1:], "DESC")
        return "{} {}".format(column, "ASC")

    def build(self):
        results = format(self.get_order_type, self.columns)

        join_orders = ", ".join(results)
        sql = "ORDER BY {}".format(join_orders)

        return sql


class Where(QueryBuilder):
    def __init__(self, **where):
        self.where = where

    def build(self):

        clauses = format("{}='{}'", self.where)

        where = " AND ".join([w for w in clauses])
        sql = "WHERE {where}".format(where=where)

        return sql


class Limit(QueryBuilder):
    def __init__(self, limit):
        self.limit = limit

    def build(self):
        return "LIMIT {}".format(self.limit)
