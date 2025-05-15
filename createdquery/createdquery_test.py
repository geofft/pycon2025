import os
import tempfile
import unittest

import createdquery


class CreatedQueryTest(unittest.TestCase):
    def test_created_query(self):
        with tempfile.TemporaryDirectory() as tempdir:
            filename = os.path.join(tempdir, "foo.txt")
            with open(filename, "w") as f:
                self.assertTrue(createdquery.was_created(f))
            with open(filename, "w") as f:
                self.assertFalse(createdquery.was_created(f))
