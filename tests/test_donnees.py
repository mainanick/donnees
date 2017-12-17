import unittest

import donnees as ds


class Users(ds.Model):
    table_name = "15"


class DonneesTests(unittest.TestCase):
    def test_klass_can_set_table_name(self):         
        self.assertTrue("15" == Users.table_name)
