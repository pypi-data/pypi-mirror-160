from abc import ABC, abstractmethod

class BaseInfer(ABC):
    @abstractmethod
    def __init__(self):
        ...
        
    @abstractmethod
    def _load_weights(self):
        ...
    
    @abstractmethod
    def __call__(self):
        ...

    @abstractmethod
    def get_session(self):
        if hasattr(self, "_model"):
            return self._model
        if hasattr(self, "_session"):
            return self._session

    @staticmethod
    def force_input(input):
        if type(input) == str:
            import imghdr
            if imghdr.what(input) is not None:
                import cv2
                input = cv2.imread(input)
        return input    