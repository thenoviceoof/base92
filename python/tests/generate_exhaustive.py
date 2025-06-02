import random
import pickle
from base92 import base92

if __name__ == "__main__":
    # Generate many random byte strings.
    encodings = []
    for _ in range(1000000):
        length = random.randint(8, 256)
        arr = bytes([random.randint(0, 255) for _ in range(length)])
        encodings.append((arr, base92.encode(arr)))

    with open("exhaustive_encodings.pickle", "wb") as pickle_file:
        pickle.dump(encodings, pickle_file)
