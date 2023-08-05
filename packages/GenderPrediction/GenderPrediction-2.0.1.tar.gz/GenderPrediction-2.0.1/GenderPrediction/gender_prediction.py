import os
import re
import numpy as np
from tensorflow.keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class GenderPredictor:
    def __init__(self, name: str, model_path: str = 'gender_model-Bilstm128-25-10-retrained.h5'):
        self.name = name
        self.model_path = model_path
        self.model = load_model(model_path)
        self.chars = list("`abcdefghijklmnopqrstuvwxyz")
        self.char2ids = {char: i for i, char in enumerate(self.chars)}
        self.ids2char = {i: char for i, char in enumerate(self.chars)}
        self.word_vec_len = 21
        self.char_len = len(self.chars)

    def preprocess(self, text: str) -> str:

        text = str(text)
        # removing '\n', '\t'
        text = re.sub("\n", "", text)
        text = re.sub("\t", "", text)

        text = text.lower()
        # Remove some punctuations
        text = re.sub(r"[!?,'\"*{})@#%(&$_.^-]", '', text)
        # Remove digits
        text = re.sub(r"\d+", "", text)

        # remove brackets
        text = re.sub(r"[\([{})\]]", "", text)

        # remove some extra
        text = re.sub(r"\u200d", "", text)

        # accuracy chars
        text = re.sub(r"[^a-z`]", "", text)

        return text

    def name_encoding(self, name: str) -> np.array:
        integer_encoded = [self.char2ids[char] for i, char in enumerate(name) if i < self.word_vec_len]
        onehot_encoded = []

        for value in integer_encoded:
            letter = [0 for _ in range(self.char_len)]
            letter[value] = 1
            onehot_encoded.append(letter)

        for _ in range(self.word_vec_len - len(name)):
            onehot_encoded.append([0 for _ in range(self.char_len)])

        return onehot_encoded

    def invert_encoding(self, encoding):
        decoded = []
        for i in encoding:
            for j, value in enumerate(i):
                if value == 1:
                    decoded.append(j)
        return "".join([self.ids2char[i] for i in decoded])

    def predict(self) -> str:
        name = self.preprocess(self.name)
        encoding = np.asarray([self.name_encoding(name)])
        probs = self.model.predict(encoding)
        if probs >= 0.5:
            return "MALE"
        elif probs < 0.5:
            return "FEMALE"
