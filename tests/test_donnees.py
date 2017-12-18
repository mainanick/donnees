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

import os
import unittest
from collections import namedtuple
from uuid import UUID

import pandas as pd
import donnees as ds
from donnees.db import QueryResult


class Contacts(ds.Model):
    table_name = "jadili_contact"
    fields = ('id', 'first_name')


class Messages(ds.Model):
    table_name = "jadili_message"
    fields = ('text', 'id', 'sentiment')
    related = (Contacts,)

class MsgKlass(ds.Model):
    table_name = "jadili_message"    


class BaseTestSetup(unittest.TestCase):
    def setUp(self):
        os.environ['DSCONFIG'] = 'postgresql://adminnickmaina:nickmaina@localhost/jadilidb'


class DonneesTests(BaseTestSetup):
    def test_klass_can_set_table_name(self):
        self.assertEqual("jadili_message", Messages.table_name)
        self.assertEqual("jadili_contact", Contacts.table_name)

    def test_klass_can_set_related(self):        
        self.assertIn(Contacts, Messages.related)
        self.assertFalse(Messages in Messages.related)

    def test_model_get(self):
        messages = Messages.get()        
        
        self.assertIsInstance(messages, QueryResult)

    def test_model_raw_query(self):
        sql = "SELECT id, text FROM jadili_message"
        messages = Messages.query(sql)
        run_sql = messages.sql
        
        self.assertEqual(sql, run_sql)

    def test_model_can_get_all_field_when_fields_is_none(self):       
        messages = MsgKlass.get()        
        expected_sql = "SELECT * FROM jadili_message"        
        
        self.assertEqual(messages.sql, expected_sql)

    def test_model_to_dataframe(self):
        messages = Messages.get(text='Test 2', sentiment=1)
        expected_sql = "SELECT text, id, sentiment FROM jadili_message WHERE text='Test 2' AND sentiment='1'"        
        
        self.assertEqual(messages.sql, expected_sql)
        self.assertIsInstance(messages.df, pd.DataFrame)
