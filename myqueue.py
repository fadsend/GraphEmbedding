class MyQueue(object):

    def __init__(self, data=None):

        assert \
            data is None or \
            type(data) == list or \
            type(data) == tuple

        if data is None:
            self.data = []
        else:
            self.data = data

    def push(self, data_to_add):
        self.data.append(data_to_add)

    def pop(self):
        return self.data.pop()

    def size(self):
        return len(self.data)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
