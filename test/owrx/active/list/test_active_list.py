from owrx.active.list import ActiveList, ActiveListIndexUpdated, ActiveListIndexAppended, ActiveListIndexDeleted
from unittest import TestCase
from unittest.mock import Mock


class ActiveListTest(TestCase):
    def testListIndexReadAccess(self):
        list = ActiveList(["testvalue"])
        self.assertEqual(list[0], "testvalue")

    def testListIndexWriteAccess(self):
        list = ActiveList(["initialvalue"])
        list[0] = "testvalue"
        self.assertEqual(list[0], "testvalue")

    def testListLength(self):
        list = ActiveList(["somevalue"])
        self.assertEqual(len(list), 1)

    def testListIndexChangeNotification(self):
        list = ActiveList(["initialvalue"])
        listenerMock = Mock()
        list.addListener(listenerMock)
        list[0] = "testvalue"
        listenerMock.onListChange.assert_called_once()
        changes, = listenerMock.onListChange.call_args.args
        self.assertEqual(len(changes), 1)
        self.assertIsInstance(changes[0], ActiveListIndexUpdated)
        self.assertEqual(changes[0].index, 0)
        self.assertEqual(changes[0].oldValue, "initialvalue")
        self.assertEqual(changes[0].newValue, "testvalue")

    def testListIndexChangeNotficationNotDisturbedByException(self):
        list = ActiveList(["initialvalue"])
        throwingMock = Mock()
        throwingMock.onListChange.side_effect = RuntimeError("this is a drill")
        list.addListener(throwingMock)
        listenerMock = Mock()
        list.addListener(listenerMock)
        list[0] = "testvalue"
        listenerMock.onListChange.assert_called_once()

    def testListAppend(self):
        list = ActiveList()
        list.append("testvalue")
        self.assertEqual(len(list), 1)
        self.assertEqual(list[0], "testvalue")

    def testListAppendNotification(self):
        list = ActiveList()
        listenerMock = Mock()
        list.addListener(listenerMock)
        list.append("testvalue")
        listenerMock.onListChange.assert_called_once()
        changes, = listenerMock.onListChange.call_args.args
        self.assertEqual(len(changes), 1)
        self.assertIsInstance(changes[0], ActiveListIndexAppended)
        self.assertEqual(changes[0].index, 0)
        self.assertEqual(changes[0].newValue, "testvalue")

    def testListDelete(self):
        list = ActiveList(["value1", "value2"])
        del list[0]
        self.assertEqual(len(list), 1)
        self.assertEqual(list[0], "value2")

    def testListDeleteNotification(self):
        list = ActiveList(["value1", "value2"])
        listenerMock = Mock()
        list.addListener(listenerMock)
        del list[0]
        listenerMock.onListChange.assert_called_once()
        changes, = listenerMock.onListChange.call_args.args
        self.assertEqual(len(changes), 1)
        self.assertIsInstance(changes[0], ActiveListIndexDeleted)
        self.assertEqual(changes[0].index, 0)
        self.assertEqual(changes[0].oldValue, 'value1')

    def testListDeleteByValue(self):
        list = ActiveList(["value1", "value2"])
        list.remove("value1")
        self.assertEqual(len(list), 1)
        self.assertEqual(list[0], "value2")

    def testListComprehension(self):
        list = ActiveList(["initialvalue"])
        x = [m for m in list]
        self.assertEqual(len(x), 1)
        self.assertEqual(x[0], "initialvalue")

    def testListenerRemoval(self):
        list = ActiveList(["initialvalue"])
        listenerMock = Mock()
        list.addListener(listenerMock)
        list[0] = "testvalue"
        listenerMock.onListChange.assert_called_once()
        listenerMock.reset_mock()
        list.removeListener(listenerMock)
        list[0] = "someothervalue"
        listenerMock.onListChange.assert_not_called()
