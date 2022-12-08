import os
import random

import numpy as np
from sklearn.metrics.pairwise import cosine_distances

from contexto.config import DATA_DIR


class Finder:
    def __init__(self):
        embeddings_path = os.path.join(DATA_DIR, 'words_embeddings.npy')
        words_path = os.path.join(DATA_DIR, 'words_filtered.txt')
        self.embeddings = np.load(embeddings_path)
        self.words = list(map(str.strip, open(words_path).readlines()))

        self.results = [
            # (word, order)
        ]

        self.word_to_distances = {}

    def get_distances(self, word: str):
        word_id = self.words.index(word)
        return cosine_distances([self.embeddings[word_id]], self.embeddings)[0]

    def find_closest(self, word_id: int, mask=None, top=10): # Not used
        if mask is None:
            mask = np.array([True] * len(self.words))

        mask[word_id] = False
        ids = np.arange(len(self.words))[mask]

        masked_words_embeddings = self.embeddings[mask]

        masked_top = np.argsort(cosine_distances([self.embeddings[word_id]], masked_words_embeddings))[0][:top + 1]

        real_top = ids[masked_top]

        return real_top

    def add_result(self, word, order):
        self.results.append((word, order))
        self.word_to_distances[word] = self.get_distances(word)

    def sample_score(self, min_gap=0.1, num_samples=50):
        scores = np.zeros(len(self.words))

        for _ in range(0, num_samples):

            word_a, order_a = random.choice(self.results)
            word_b, order_b = random.choice(self.results)

            if order_a < order_b * (1.0 - min_gap):
                scores += (self.word_to_distances[word_a] - self.word_to_distances[word_b] < 0)

            if order_a > order_b * (1.0 + min_gap):
                scores += (self.word_to_distances[word_a] - self.word_to_distances[word_b] > 0)

        top_score = max(scores)
        # top_score = np.percentile(scores, 90)

        while True:
            mask = scores >= top_score

            for word, _ in self.results:
                word_id = self.words.index(word)
                mask[word_id] = False

            closest_ids = np.arange(len(self.words))[mask]
            if len(closest_ids) > 0:
                break
            else:
                top_score -= 1

        return closest_ids

    def guess_next(self):
        closest = self.sample_score(min_gap=0.5, num_samples=500)
        return self.words[closest[0]]


if __name__ == '__main__':
    results = [
    ]

    finder = Finder()

    # ctrl+c handler:
    import signal
    import sys


    def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        print('Results:')
        print(finder.results)
        sys.exit(0)


    signal.signal(signal.SIGINT, signal_handler)

    for word, order in results:
        finder.add_result(word, order)

    if len(finder.results) == 0:
        word = input('Word: ')
        order = int(input('Order: '))
        finder.add_result(word, order)

    while True:
        next_word = finder.guess_next()
        print(next_word)
        try:
            order = int(input('Order: '))
        except ValueError as e:
            print('Invalid order')
            continue

        finder.add_result(next_word, order)


