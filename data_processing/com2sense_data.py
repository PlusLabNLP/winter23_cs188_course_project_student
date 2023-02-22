import os
import sys
import json
import csv
import glob
import pprint
import numpy as np
import random
import argparse
from tqdm import tqdm
from .utils import DataProcessor
from .utils import Coms2SenseSingleSentenceExample
from transformers import (
    AutoTokenizer,
)


class Com2SenseDataProcessor(DataProcessor):
    """Processor for Com2Sense Dataset.
    Args:
        data_dir: string. Root directory for the dataset.
        args: argparse class, may be optional.
    """

    def __init__(self, data_dir=None, args=None, **kwargs):
        """Initialization."""
        self.args = args
        self.data_dir = data_dir

        # TODO: Label to Int mapping, dict type.
        self.label2int = {"True": 1, "False": 0}

    def get_labels(self):
        """See base class."""
        return 2  # Binary.

    def _read_data(self, data_dir=None, split="train"):
        """Reads in data files to create the dataset."""
        if data_dir is None:
            data_dir = self.data_dir

        examples = []   # Store your examples in this list

        ##################################################
        # TODO:
        # Some instructions for reading data:
        # 1. Use json python package to load the data properly.
        # 2. Use the provided class `Coms2SenseSingleSentenceExample` 
        # in `utils.py` for creating examples
        # 3. Store the two complementary statements as two 
        # individual examples 
        # e.g. example_1 = ...
        #      example_2 = ...
        #      examples.append(example_1)
        #      examples.append(example_2)
        # 4. Make sure that the order is maintained.
        # i.e. sent_1 in the data is stored/appended first and
        # sent_2 in the data is stored/appened after it.
        # 5. For the guid, simply use the row number (0-
        # indexed) for each data instance.
        # Use the same guid for statements from the same complementary pair.
        # 6. Make sure to handle if data do not have labels field.
        # This is useful for loading test data
        # End of TODO.
        ##################################################
        json_path = os.path.join(data_dir, split+'.json')
        data = json.load(open(json_path, 'r'))

        for index, datum in enumerate(data[:3]):
            guid = index
            text_1 = datum.get("sent_1")
            text_2 = datum.get("sent_2")

            label_1 = self.label2int[datum["label_1"]] if "label_1" in datum else None
            label_2 = self.label2int[datum["label_2"]] if "label_2" in datum else None

            domain = datum.get("domain", None)
            scenario = datum.get("scenario", None)
            numeracy = datum["numeracy"]=="True" if "numeracy" in datum else None

            example_1 = Coms2SenseSingleSentenceExample(
                guid, text_1, 
                label=label_1, 
                domain=domain, 
                scenario=scenario, 
                numeracy=numeracy
            )
            example_2 = Coms2SenseSingleSentenceExample(
                guid, text_2, 
                label=label_2, 
                domain=domain, 
                scenario=scenario, 
                numeracy=numeracy
            )

            examples.append(example_1)
            examples.append(example_2)

        return examples

    def get_train_examples(self, data_dir=None):
        """See base class."""
        return self._read_data(data_dir=data_dir, split="train")

    def get_dev_examples(self, data_dir=None):
        """See base class."""
        return self._read_data(data_dir=data_dir, split="dev")

    def get_test_examples(self, data_dir=None):
        """See base class."""
        return self._read_data(data_dir=data_dir, split="test")


if __name__ == "__main__":

    # Test loading data.
    proc = Com2SenseDataProcessor(data_dir="datasets/com2sense")
    train_examples = proc.get_train_examples()
    val_examples = proc.get_dev_examples()
    test_examples = proc.get_test_examples()
    print()
    for i in range(3):
        print(test_examples[i])
    print()
