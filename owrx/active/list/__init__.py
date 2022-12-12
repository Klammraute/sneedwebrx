from abc import ABC, abstractmethod

import logging
logger = logging.getLogger(__name__)


class ActiveListListener(ABC):
    @abstractmethod
    def onIndexChanged(self, index, newValue):
        pass

    @abstractmethod
    def onAppend(self, newValue):
        pass

    @abstractmethod
    def onDelete(self, index):
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
        for listener in self.listeners:
            try:
                listener.onAppend(value)
            except Exception:
                logger.exception("Exception during onAppend notification")

    def remove(self, value):
        self.__delitem__(self.delegate.index(value))

    def __setitem__(self, key, value):
        self.delegate[key] = value
        for listener in self.listeners:
            try:
                listener.onIndexChanged(key, value)
            except Exception:
                logger.exception("Exception during onKeyChanged notification")

    def __delitem__(self, key):
        del self.delegate[key]
        for listener in self.listeners:
            try:
                listener.onDelete(key)
            except Exception:
                logger.exception("Exception during onDelete notification")

    def __getitem__(self, key):
        return self.delegate[key]

    def __len__(self):
        return len(self.delegate)

    def __iter__(self):
        return self.delegate.__iter__()
