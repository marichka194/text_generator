from collections import deque
import codecs


class TripleReader(object):

    def __init__(self, filename):
        self.filename = filename
        self.buffer = deque()
        self.file = None
        self.gen_read = self._read()

        for word in self.gen_read:
            self.buffer.append(word)
            if len(self.buffer) == 2:
                break

    def _read(self):

        if self.file is None:
            self.file = codecs.open(self.filename, encoding='utf-8')

        for line in self.file:
            for word in line.strip().split():
                clean_word = word.strip().lower()
                if len(clean_word) > 1 and (not clean_word[1].isalpha() or not clean_word[-1].isalpha()):
                    continue
                else:
                    yield clean_word

    def read_triple(self):
        for word in self.gen_read:
            self.buffer.append(word)
            yield list(self.buffer)
            self.buffer.popleft()

