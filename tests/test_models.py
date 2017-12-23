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

import pandas as pd

from donnees.db import QueryResult
from tests import models


class BaseTestSetup(unittest.TestCase):
    def setUp(self):
        os.environ['DSCONFIG'] = 'postgresql://adminnickmaina:nickmaina@localhost/jadilidb'


class DonneesTests(BaseTestSetup):
    def test_klass_can_set_table_name(self):
        self.assertEqual("jadili_message", models.Messages.table_name)
        self.assertEqual("jadili_contact", models.Contacts.table_name)

    def test_klass_can_set_related(self):
        self.assertIn(models.Contacts, models.Messages.related)
        self.assertFalse(models.Messages in models.Messages.related)

    def test_model_query_set(self):
        messages = models.Messages.get()
        self.assertIsInstance(messages, QueryResult)

    def test_models_query_set_result_is_list(self):
        messages = models.Messages.get()
        self.assertIsInstance(messages.results, list)

    def test_model_raw_query(self):
        sql = "SELECT id, text FROM jadili_message"

        sql2 = "SELECT \
            jadili_message.id, \
            jadili_message.text, \
            jadili_message.created_on \
            FROM jadili_message \
            FULL OUTER JOIN jadili_contact ON jadili_message.contact_id = jadili_contact.id;"

        messages = models.Messages.query(sql)
        messages2 = models.Messages.query(sql2)

        run_sql = messages.sql
        run_sql2 = messages2.sql

        self.assertEqual(sql, run_sql)
        self.assertEqual(sql2, run_sql2)
        self.assertIsInstance(messages.df, pd.DataFrame)
        self.assertIsInstance(messages2.df, pd.DataFrame)

    def test_model_can_get_all_field_when_fields_is_none(self):
        messages = models.MsgKlass.get()
        expected_sql = "SELECT * FROM jadili_message"

        self.assertEqual(messages.sql, expected_sql)

    def test_model_to_dataframe(self):
        messages = models.MsgKlass.get()
        expected_sql = "SELECT * FROM jadili_message"

        self.assertIsInstance(messages.df, pd.DataFrame)

    def test_get_select_where(self):
        messages = models.Messages.get(text='Test 2', sentiment=1)
        messages2 = models.Messages.get(text='Test 2')
        expected_sql = "SELECT jadili_message.text, jadili_message.sentiment FROM jadili_message WHERE jadili_message.text='Test 2' AND jadili_message.sentiment='1';"
        expected_sql2 = "SELECT jadili_message.text, jadili_message.sentiment FROM jadili_message WHERE jadili_message.text='Test 2';"

        self.assertEqual(messages.sql, expected_sql)
        self.assertEqual(messages2.sql, expected_sql2)