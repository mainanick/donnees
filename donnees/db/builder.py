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

from donnees.utils import Attrvalue

JOIN = Attrvalue({'INNER':"INNER JOIN", 'OUTER':"OUTER JOIN"})


class QueryBuilder(object):
    def build(self):
        raise NotImplementedError


class Select(QueryBuilder):    
    def __init__(self, columns, table, clauses):
        self.clauses = clauses        
    
    def build(self):
        sql= "SELECT {columns} FROM {table} {clauses};"
        for clause in self.clauses:
            sql +=clause.build()       
        return "built"


class Join(QueryBuilder):
    def __init__(self, join_by):        
        self.join = join_by
    
    def build(self):        
        sql = JOIN.INNER + " {table} ON {fields} "
        pass


class Order(QueryBuilder):
    def __init__(self, columns, order_type=None):
        self.columns = columns
        self.order = order_type
    
    def build(self):
        sql = " ORDER BY {columns} {order_type}"
        pass


class Where(QueryBuilder):
    def __init__(self, where):
        self.where = where
    
    def build(self):
        pass