import tensorflow_hub as hub
import tensorflow_text


def load_model():
    print('loading model')
    return hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3")


def calc_dist(a, b):
    total = 0
    for i in range(len(a)):
        total += (a[i] - b[i])**2
    return total ** 0.5
