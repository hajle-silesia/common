import json
import os
import pathlib
import unittest

import common.storage
import common.utils


class TestStorage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_test_expected_results()

    @classmethod
    def set_test_arguments(cls):
        cls.storage_path = pathlib.Path(__file__).parent / "./data.json"
        cls.data = {'key_1': "value_1", 'key_2': "values_2", 'key_3': "values_3"}

    @classmethod
    def set_tested_objects(cls):
        pass

    @classmethod
    def set_test_expected_results(cls):
        pass

    def setUp(self):
        super().setUp()

        self.storage = common.storage.Storage()

    def tearDown(self):
        super().tearDown()

        common.utils.remove_file(self.storage_path)

    def test_Should_GetEmptyPath_When_PathWasNotSet(self):
        self.assertEqual("", self.storage.path)

    def test_Should_GetPath_When_PathWasSet(self):
        self.storage.path = self.storage_path

        self.assertEqual(self.storage_path, self.storage.path)

    def test_Should_NotCreateDataFile_When_PathAndDataWereNotSet(self):
        self.assertEqual(False, os.path.exists(self.storage_path))

    def test_Should_NotCreateDataFile_When_PathWasNotSet(self):
        self.storage.dump_data(self.data)

        self.assertEqual(False, os.path.exists(self.storage_path))

    def test_Should_CreateDataFile_When_DataIsNone(self):
        self.storage.path = self.storage_path
        self.storage.dump_data(None)

        self.assertEqual(True, os.path.exists(self.storage_path))

    def test_Should_CreateDataFile_When_DataIsEmpty(self):
        self.storage.path = self.storage_path
        self.storage.dump_data("")

        self.assertEqual(True, os.path.exists(self.storage_path))

    def test_Should_DumpData_When_DataIsNone(self):
        self.storage.path = self.storage_path
        self.storage.dump_data(None)

        with open(self.storage_path, encoding="utf-8") as data_json:
            data = json.load(data_json)

        self.assertEqual(None, data)

    def test_Should_DumpData_When_DataIsNonempty(self):
        self.storage.path = self.storage_path
        self.storage.dump_data(self.data)

        with open(self.storage_path, encoding="utf-8") as data_json:
            data = json.load(data_json)

        self.assertEqual(self.data, data)

    def test_Should_LoadNoData_When_InvokedForNonexistentFile(self):
        self.storage.path = self.storage_path

        self.assertEqual(None, self.storage.load_data())

    def test_Should_LoadData_When_InvokedForExistingFile(self):
        data = "test_data"
        with open(self.storage_path, "w", encoding="utf-8") as data_json:
            json.dump(data, data_json)

        self.storage.path = self.storage_path

        self.assertEqual(data, self.storage.load_data())
