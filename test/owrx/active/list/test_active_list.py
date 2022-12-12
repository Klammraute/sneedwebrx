from owrx.active.list import ActiveList
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
        listenerMock.onIndexChanged.assert_called_once_with(0, "testvalue")

    def testListIndexChangeNotficationNotDisturbedByException(self):
        list = ActiveList(["initialvalue"])
        throwingMock = Mock()
        throwingMock.onIndexChanged.side_effect = RuntimeError("this is a drill")
        list.addListener(throwingMock)
        listenerMock = Mock()
        list.addListener(listenerMock)
        list[0] = "testvalue"
        listenerMock.onIndexChanged.assert_called_once_with(0, "testvalue")

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
        listenerMock.onAppend.assert_called_once_with("testvalue")

    def testListDelete(self):
        list = ActiveList(["value1", "value2"])
        del list[0]
        self.assertEqual(len(list), 1)
        self.assertEqual(list[0], "value2")

    def testListDelteNotification(self):
        list = ActiveList(["value1", "value2"])
        listenerMock = Mock()
        list.addListener(listenerMock)
        del list[0]
        listenerMock.onDelete.assert_called_once_with(0)

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
        listenerMock.onIndexChanged.assert_called_once_with(0, "testvalue")
        listenerMock.reset_mock()
        list.removeListener(listenerMock)
        list[0] = "someothervalue"
        listenerMock.onIndexChanged.assert_not_called()
