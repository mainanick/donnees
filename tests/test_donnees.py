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
        messages = Messages.get(name='Nick')
        
        self.assertIsInstance(messages[0].id, UUID)
        self.assertIsInstance(messages, QueryResult)

    def test_model_raw_query(self):
        sql = "SELECT id, text FROM jadili_message"
        messages = Messages.query(sql)
        run_sql = messages.sql
        
        self.assertEqual(sql, run_sql)

    def test_model_get_all_field(self):
        pass

    def test_model_get_related(self):
        pass

    def test_model_to_dataframe(self):
        messages = Messages.get(name='Nick')
        dataframe = messages.df
        
        self.assertIsInstance(dataframe, pd.DataFrame)
