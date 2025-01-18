
class BasketIterator:
    def __init__(self, basket):
        self._basket = basket
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._basket):
            result = self._basket[self._index]
            self._index += 1
            return result
        raise StopIteration