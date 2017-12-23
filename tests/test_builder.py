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

import unittest

from donnees.db import builder


class DonneesQueryTests(unittest.TestCase):
    def test_build_where(self):
        sql = builder.Where(age=18, name="nick").build()

        self.assertEqual("WHERE age='18' AND name='nick'", sql)
        self.assertFalse("WHERE x='1'" == sql)

    def test_build_order(self):
        sql = builder.Order("-age").build()
        sql2 = builder.Order("age", "-name").build()

        self.assertEqual("ORDER BY age DESC", sql)
        self.assertEqual("ORDER BY age ASC, name DESC", sql2)

    def test_build_inner_join(self):
        expected_sql = "INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID"
        sql = builder.Join("Orders", "CustomerID",
                           "Customers",  "CustomerID").build()
        self.assertEqual(expected_sql, sql)

    def test_build_select_without_clauses(self):
        expected_sql = "SELECT * FROM message;"
        sql = builder.Select("message").build()
        self.assertEqual(expected_sql, sql)

    def test_build_select_with_clauses(self):
        expected_sql = "SELECT * FROM message WHERE name='nick';"
        expected_sql2 = "SELECT * FROM message WHERE name='nick' INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID;"

        where = builder.Where(name="nick")
        sql = builder.Select("message", "*", where).build()

        join = builder.Join("Orders", "CustomerID", "Customers",  "CustomerID")
        sql2 = builder.Select("message", "*", where, join).build()

        self.assertEqual(expected_sql, sql)
        self.assertEqual(expected_sql2, sql2)
