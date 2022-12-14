from abc import ABC, abstractmethod

import logging
logger = logging.getLogger(__name__)


class ActiveListChange(ABC):
    pass


class ActiveListIndexUpdated(ActiveListChange):
    def __init__(self, index: int, oldValue, newValue):
        self.index = index
        self.oldValue = oldValue
        self.newValue = newValue


class ActiveListIndexAppended(ActiveListChange):
    def __init__(self, index: int, newValue):
        self.index = index
        self.newValue = newValue


class ActiveListIndexDeleted(ActiveListChange):
    def __init__(self, index: int, oldValue):
        self.index = index
        self.oldValue = oldValue


class ActiveListListener(ABC):
    @abstractmethod
    def onListChange(self, changes: list[ActiveListChange]):
        pass


class ActiveList:
    def __init__(self, elements: list = None):
        self.delegate = elements.copy() if elements is not None else []
        self.listeners = []

    def addListener(self, listener: ActiveListListener):
        if listener in self.listeners:
            return
        self.listeners.append(listener)

    def removeListener(self, listener: ActiveListListener):
        if listener not in self.listeners:
            return
        self.listeners.remove(listener)

    def append(self, value):
        self.delegate.append(value)
        self.__fireChanges([ActiveListIndexAppended(len(self) - 1, value)])

    def __fireChanges(self, changes: list[ActiveListChange]):
        for listener in self.listeners:
            try:
                listener.onListChange(changes)
            except Exception:
                logger.exception("Exception during onListChange notification")

    def remove(self, value):
        self.__delitem__(self.delegate.index(value))

    def __setitem__(self, key, value):
        if self.delegate[key] == value:
            return
        oldValue = self.delegate[key]
        self.delegate[key] = value
        self.__fireChanges([ActiveListIndexUpdated(key, oldValue, value)])

    def __delitem__(self, key):
        oldValue = self.delegate[key]
        del self.delegate[key]
        self.__fireChanges([ActiveListIndexDeleted(key, oldValue)])

    def __getitem__(self, key):
        return self.delegate[key]

    def __len__(self):
        return len(self.delegate)

    def __iter__(self):
        return self.delegate.__iter__()
