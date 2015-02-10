from unittest import TestCase
from XALTdb import XALTdb
import os
import json
import ConfigParser
from xalt_db_model import XALT_link, XALT_run, XALT_env_name, XALT_object

class TestXALTdb(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.link_obj = json.load(open(os.path.join(os.path.dirname(__file__), 'xaltdb_test_data/link.json')))
        cls.run_obj = json.load(open(os.path.join(os.path.dirname(__file__), 'xaltdb_test_data/run.json')))
        cls.reverseMap = json.load(open(os.path.join(os.path.dirname(__file__), 'xaltdb_test_data/reverseMap.json')))

    def setUp(self):
        self.db_class = XALTdb(os.path.join(os.path.dirname(__file__), 'xalt_db_test_memory.conf'))

    def test_initialize_with_wrong_config_file(self):
        with self.assertRaises(ConfigParser.Error) as context:
            XALTdb('xalt_db_test_memoryr.conf')
        self.assertEqual(context.exception.message, "No section: 'DATABASE'")

    def test_connect(self):
        self.db_class.connect()

    def test_connection_string(self):
        self.assertEqual(self.db_class.connection_string(), 'sqlite:///:memory:')

    def test_link_to_db(self):
        XALTdb.link_to_db(self.db_class, self.reverseMap, self.link_obj)
        session = self.db_class._XALTdb__sessionmaker()
        session.query(XALT_link).filter(XALT_link.uuid == '3394fef0-4b67-44ba-8532-a4646ffcc251').one()
        self.assertEqual(session.query(XALT_object).count(), 12)

    def test_run_to_db(self):
        self.test_link_to_db()
        XALTdb.run_to_db(self.db_class, self.reverseMap, self.run_obj)
        session = self.db_class._XALTdb__sessionmaker()
        session.query(XALT_link).filter(XALT_link.uuid == '3394fef0-4b67-44ba-8532-a4646ffcc251').one()
        session.query(XALT_run).filter(XALT_run.run_uuid == 'fc5c39da-6d24-4926-8687-90a072a5bd37').one()
        self.assertEqual(session.query(XALT_object).count(), 13)
        self.assertEqual(session.query(XALT_env_name).count(), 92)