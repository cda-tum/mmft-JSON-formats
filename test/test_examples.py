import unittest
import os
import sys

sys.path.append("src/")
from mmft_model import MMFTDataModel
from pydantic import ValidationError

class TestExamples(unittest.TestCase):

    def test_examples(self):
        d = 'examples'
        r = []
        for file in os.listdir(d):
            filename = os.fsdecode(file)
            if filename.endswith(".json"):
                with open(os.path.join(d, file), "r") as file:
                    content = file.read()
                    try:
                        MMFTDataModel.model_validate_json(content)
                        valid = True
                        errors = None
                    except ValidationError as e:
                        errors = e
                        valid = False

                    r.append((file, valid, errors))

        if any([lambda f: not f[1], r]):
            self.fail(r)