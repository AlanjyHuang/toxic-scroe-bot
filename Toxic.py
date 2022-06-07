from keras.models import load_model
from keras.preprocessing import text
from keras_preprocessing import sequence
import pandas as pd


class Toxic:
    def __init__(self):
        # model
        self.model = load_model("model.hdf5")
        self.maxlen = 150
        max_features = 100000

        # tokenizer
        train = pd.read_csv("train.csv")
        test = pd.read_csv("test.csv")
        train["comment_text"].fillna("fillna")
        test["comment_text"].fillna("fillna")
        X_train = train["comment_text"].str.lower()
        X_test = test["comment_text"].str.lower()
        self.tok = text.Tokenizer(num_words=max_features, lower=True)
        self.tok.fit_on_texts(list(X_train)+list(X_test))

        del train
        del test
        del X_train
        del X_test

    def predict(self, s: str):
        s_tok = [s.lower()]
        s_tok = self.tok.texts_to_sequences(s)
        s_tok = sequence.pad_sequences(s_tok, maxlen=self.maxlen)

        return self.model.predict(s_tok)
