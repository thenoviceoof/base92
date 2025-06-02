import unittest
import sys
import os
import pickle

from base92 import base92


class TestBase92Exhaustive(unittest.TestCase):
    """Test against an existing dictionary of random encodings/decodings.

    Ideally we would check in this data as a golden standard, but:
    #1 It is 290MB.
    #2 This is more of a paranoia check; the chances we catch a
       problem with 1 million random checks is probably
       infinitesimally larger than with 1000 checks.
    #3 If we really wanted confidence, we should write a proof.

    """

    # Tox does not run this by default, but better safe than sorry.
    @unittest.skipUnless(
        os.getenv("RUN_EXHAUSTIVE_TESTS"),
        "Skipping expensive test (set RUN_EXHAUSTIVE_TESTS=1 to run)",
    )
    def test_exhaustive(self):
        with open("exhaustive_encodings.pickle", "rb") as pickle_file:
            encodings = pickle.load(pickle_file)

        for source, target in encodings:
            encoded = base92.encode(source)
            self.assertEqual(
                target,
                encoded,
                f"Does not match golden data: from {source}, expected {target}, got {encoded}",
            )
            decoded = base92.decode(encoded)
            self.assertEqual(
                source,
                decoded,
                f"Does not match golden data: from {target}, expected {source}, got {decoded}",
            )
