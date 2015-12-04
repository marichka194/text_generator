from collections import defaultdict
from random import choice
import itertools
import cPickle
import zlib
import logging
import argparse

import reader


class Node(object):
    __slots__ = ["count", "next_word", "after_one"]

    def __init__(self):
        self.count = 1
        self.next_word = defaultdict(Node)
        self.after_one = defaultdict(Node)


class StatisticsStorage(object):
    __slots__ = ["tree"]

    def __init__(self):
        self.tree = defaultdict(Node)

    def insert(self, word1, word2, word3):
        self.tree[word1].count += 1
        self.tree[word1].next_word[word2].count += 1
        self.tree[word1].after_one[word3].count += 1

    def get(self, word1, word2):
        word1_dict = self.tree[word1].after_one
        word2_dict = self.tree[word2].next_word
        results_generator = itertools.chain.from_iterable(
            itertools.repeat(word, min(word1_dict[word].count, word2_dict[word].count))
            for word in word1_dict if word in word2_dict
        )

        all_results = list(results_generator)
        if not all_results:
            all_results = list(
                itertools.chain.from_iterable(itertools.repeat(word, node.count)
                                              for word, node in self.tree.iteritems())
            )
        return choice(all_results)


def dump(stats, filename):
    data = cPickle.dumps(stats, -1)
    compressed = zlib.compress(data)
    with open(filename, "wb") as dump_file:
        dump_file.write(compressed)


def read(filename):
    with open(filename, "rb") as dump_file:
        content = dump_file.read()
    decompressed = zlib.decompress(content)
    return cPickle.loads(decompressed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", required=True, help="Source file with text")
    parser.add_argument("-d", "--dst", required=False, default="stats.dump", help="Output file for processed statistics")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)
    logging.info("Dump stats...")
    storage = StatisticsStorage()
    file_reader = reader.TripleReader(args.src)
    logging.info("read data file")
    for (w1, w2, w3) in file_reader.read_triple():
        storage.insert(w1, w2, w3)
    logging.info("storage ready")
    logging.info("start pickling")
    dump(storage, args.dst)
