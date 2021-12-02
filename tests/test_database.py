from engine.storages import TagStorage
import unittest
import time
import sys
import shutil
import os


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.tag_storage = TagStorage()


    def test_database(self):
        tag_1 = TagMessage('sdfsdfs', 'key', 'value', 5498694, 'klIel49$')
        tag_2 = TagMessage('jsokclksdb', 'key2', 'value2', 8490609, 'ipblelkc')
        self.tag_storage.put_tag(tag_1)
        self.tag_storage.put_tag(tag_2)



    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()