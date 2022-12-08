import os

import gensim.downloader as downloader
import numpy as np

from contexto.config import DATA_DIR


def main():
    w2v = downloader.load('word2vec-google-news-300')

    words = list(
        map(
            str.lower,
            map(str.strip, open(os.path.join(DATA_DIR, 'words.txt')).readlines())
        )
    )

    words = [word for word in words if word in w2v]

    words_embeddings = np.stack([
        w2v[word] for word in words if word in w2v
    ])

    np.save(os.path.join(DATA_DIR, 'words_embeddings.npy'), words_embeddings)

    # Save filtered words
    with open(os.path.join(DATA_DIR, 'words_filtered.txt'), 'w') as f:
        f.write('\n'.join(words))


if __name__ == '__main__':
    main()
