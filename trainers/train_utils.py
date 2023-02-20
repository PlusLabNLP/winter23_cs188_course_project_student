import csv
import glob
import json
import random
import logging
import os
from enum import Enum
from typing import List, Optional, Union
from sklearn import metrics

import tqdm
import numpy as np

import torch
from transformers import (
    WEIGHTS_NAME,
    AdamW,
    AutoConfig,
    AutoModelForMaskedLM,
    AutoTokenizer,
)

def evaluate_standard(preds, labels, scoring_method):

    # The accuracy, precision, recall and F1 scores to return
    acc, prec, recall, f1 = 0.0, 0.0, 0.0, 0.0

    ########################################################
    # You need to compute the accuracy, precision, recall
    # and F1 score for the predictions and gold labels.
    # Please also make your sci-kit learn scores are computed
    # using `scoring_method` for the `average` argument.
    acc = metrics.accuracy_score(y_true=labels, y_pred=preds)
    prec = metrics.precision_score(y_true=labels, y_pred=preds, average=scoring_method)
    recall = metrics.recall_score(y_true=labels, y_pred=preds, average=scoring_method)
    f1 = metrics.f1_score(y_true=labels, y_pred=preds, average=scoring_method)
    ########################################################

    return acc, prec, recall, f1

def pairwise_accuracy(guids, preds, labels):

    acc = 0.0  # The accuracy to return.
    
    ########################################################
    # Please finish the pairwise accuracy computation.
    # Hint: Utilize the `guid` as the `guid` for each
    # statement coming from the same complementary
    # pair is identical. You can simply pair the these
    # predictions and labels w.r.t the `guid`. 
    guid_to_num_correct = {}
    for guid, pred, label in zip(guids, preds, labels):
        if guid not in guid_to_num_correct:
            guid_to_num_correct[guid] = 0
        if pred == label:
            guid_to_num_correct[guid] += 1

    correct_preds = 0
    for _, num_correct in guid_to_num_correct.items():
        if num_correct == 2: # both pairs must be correct
            correct_preds += 1
    acc = correct_preds / len(guid_to_num_correct)
    ########################################################
     
    return acc

if __name__ == "__main__":

    # Unit-testing the pairwise accuracy function.
    guids = [0, 0, 1, 1, 2, 2, 3, 3]
    preds = np.asarray([0, 0, 1, 0, 0, 1, 1, 1])
    labels = np.asarray([1, 0, 1, 1, 0, 1, 1, 1])
    acc, prec, rec, f1 = evaluate_standard(preds, labels, "binary")
    pair_acc = pairwise_accuracy(guids, preds, labels)

    if acc == 0.75 and prec == 1.0 and round(rec,2) == 0.67 and f1 == 0.8:
        print("Your `evaluate_standard` function is correct!")
    else:
        raise NotImplementedError("Your `evaluate_standard` function is INCORRECT!")

    if pair_acc == 0.5:
        print("Your `pairwise_accuracy` function is correct!")
    else:
        raise NotImplementedError("Your `pairwise_accuracy` function is INCORRECT!")
