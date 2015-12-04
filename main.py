import logging
import codecs
import re
import argparse
import random

from core.stats import StatisticsStorage, Node, read


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--src", required=True, help="Stats dump file")
    parser.add_argument("-d", "--dst", required=True, help="Output file for generated text")
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)
    logging.info("load stats")
    storage = read(args.src)
    logging.info("stats loaded")
    logging.info("init system")
    w1 = storage.get("_", "_")
    w2 = storage.get("_", "_")
    w3 = storage.get(w1, w2)
    logging.info("start generating")
    result = []
    for i in range(15000):
        result.append(w3)
        w1, w2, w3 = w2, w3, storage.get(w1, w2)
    logging.info("text generated")
    for index, word in enumerate(result):
        if index > 0:
            if result[index - 1] in [".", "!", "?"]:
                if result[index] in [".", "!", "?"]:
                    result[index] = ""
                    continue
                result[index] = word.capitalize()
                if random.random() > 0.9:
                    result[index - 1] += "\n"
        else:
            result[index] = word.capitalize()

    text = u" ".join(result)
    if not text.endswith(u"."):
        text += u"."
    corrected_text = re.sub(r"\s\.", r".", text, flags=re.UNICODE)
    logging.info("start saving to disk")
    with codecs.open(args.dst, "w", encoding="utf-8") as f:
        f.write(corrected_text)
    logging.info("finished")
