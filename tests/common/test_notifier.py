import json
import os
import pathlib
import unittest.mock

import common.notifier
import common.storage
import common.utils

url_1 = {'observer_1': "http://observer_1/update"}
url_2 = {'observer_2': "http://observer_2/update"}
url = url_1 | url_2


def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] in url.values():
        return MockResponse(None, 204)
    else:
        raise TimeoutError


@unittest.mock.patch("common.notifier.requests.post", side_effect=mocked_requests_post)
class TestNotifier(unittest.TestCase):
    storage_path = None
    storage = None

    @classmethod
    def setUpClass(cls):
        cls.set_test_arguments()
        cls.set_tested_objects()
        cls.set_test_expected_results()

    @classmethod
    def set_test_arguments(cls):
        cls.storage_path = pathlib.Path(__file__).parent / "./data.json"
        cls.storage = common.storage.Storage()
        cls.storage.path = cls.storage_path

    @classmethod
    def set_tested_objects(cls):
        pass

    @classmethod
    def set_test_expected_results(cls):
        pass

    def setUp(self):
        super().setUp()

        self.notifier = common.notifier.Notifier(self.storage)

    def tearDown(self):
        super().tearDown()

        common.utils.remove_file(self.storage_path)

    def test_Should_GetEmptyObservers_When_ObserversWereNotAdded(self, mock_get):
        self.assertEqual({}, self.notifier.observers)

    def test_Should_NotGetObserversFile_When_ObserversWereNotAdded(self, mock_get):
        self.assertEqual(False, os.path.exists(self.storage_path))

    def test_Should_GetObservers_When_ObserverWasAdded(self, mock_get):
        self.notifier.register_observer(url_1)

        self.assertEqual(url_1, self.notifier.observers)

    def test_Should_GetObserversFile_When_ObserverWasAdded(self, mock_get):
        self.notifier.register_observer(url_1)

        self.assertEqual(True, os.path.exists(self.storage_path))

    def test_Should_DumpObservers_When_ObserverWasAdded(self, mock_get):
        self.notifier.register_observer(url_1)

        with open(self.storage_path, encoding="utf-8") as data_json:
            data = json.load(data_json)

        self.assertEqual(url_1, data)

    def test_Should_GetOneObserver_When_TheSameObserverWasAdded(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.register_observer(url_1)

        self.assertEqual(url_1, self.notifier.observers)

    def test_Should_GetObserversFile_When_TheSameObserverWasAdded(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.register_observer(url_1)

        self.assertEqual(True, os.path.exists(self.storage_path))

    def test_Should_DumpObservers_When_TheSameObserverWasAdded(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.register_observer(url_1)

        with open(self.storage_path, encoding="utf-8") as data_json:
            data = json.load(data_json)

        self.assertEqual(url_1, data)

    def test_Should_GetTwoObservers_When_TwoObserversWereAdded(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.register_observer(url_2)

        self.assertEqual(url_1 | url_2, self.notifier.observers)

    def test_Should_GetObserversFile_When_TwoObserversWereAdded(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.register_observer(url_2)

        self.assertEqual(True, os.path.exists(self.storage_path))

    def test_Should_DumpObservers_When_TwoObserversWereAdded(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.register_observer(url_2)

        with open(self.storage_path, encoding="utf-8") as data_json:
            data = json.load(data_json)

        self.assertEqual(url_1 | url_2, data)

    def test_Should_GetEmptyObservers_When_ObserverWasAddedAndRemoved(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.remove_observer(url_1)

        self.assertEqual({}, self.notifier.observers)

    def test_Should_GetObserversFile_When_ObserverWasAddedAndRemoved(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.remove_observer(url_1)

        self.assertEqual(True, os.path.exists(self.storage_path))

    def test_Should_DumpObservers_When_ObserverWasAddedAndRemoved(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.remove_observer(url_1)

        with open(self.storage_path, encoding="utf-8") as data_json:
            data = json.load(data_json)

        self.assertEqual({}, data)

    def test_Should_GetEmptyResponses_When_ClassInstanceWasCreated(self, mock_get):
        self.assertEqual([], self.notifier.responses)

    def test_Should_HandleTimeoutException_When_UnknownObserverWasRegisteredAndNotifyTimedOut(self, mock_get):
        self.notifier.register_observer({'unknown_observer': "http://unknown_observer/update"})
        self.notifier.notify_observers("test_data")

        self.assertEqual(1, len(self.notifier.responses))
        self.assertEqual(None, self.notifier.responses[0])

    def test_Should_NotifyObserver_When_OneObserverWasRegisteredAndNotifyWasInvoked(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.notify_observers("test_data")

        self.assertEqual(1, len(self.notifier.responses))
        self.assertEqual(204, self.notifier.responses[0].status_code)
        self.assertEqual(None, self.notifier.responses[0].json())

    def test_Should_NotifyObservers_When_MultipleObserversWereRegisteredAndNotifyWasInvoked(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.register_observer(url_2)
        self.notifier.notify_observers("test_data")

        self.assertEqual(2, len(self.notifier.responses))
        for response in self.notifier.responses:
            self.assertEqual(204, response.status_code)
            self.assertEqual(None, response.json())

    def test_Should_LoadObservers_When_CreatingClassInstance(self, mock_get):
        with open(self.storage_path, "w", encoding="utf-8") as data_json:
            json.dump(url_1, data_json)

        storage = common.storage.Storage()
        storage.path = self.storage_path
        notifier = common.notifier.Notifier(storage)

        self.assertEqual(url_1, notifier.observers)

    def test_Should_ClearResponses_When_NotifyIsInvokedMultipleTimes(self, mock_get):
        self.notifier.register_observer(url_1)
        self.notifier.notify_observers("test_data")

        self.assertEqual(1, len(self.notifier.responses))
        self.assertEqual(204, self.notifier.responses[0].status_code)
        self.assertEqual(None, self.notifier.responses[0].json())

        self.notifier.notify_observers("test_data")

        self.assertEqual(1, len(self.notifier.responses))
        self.assertEqual(204, self.notifier.responses[0].status_code)
        self.assertEqual(None, self.notifier.responses[0].json())
