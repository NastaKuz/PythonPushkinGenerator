from itertools import zip_longest

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow import keras
from tensorflow.keras.layers import *
import tensorflow as tf
import numpy as np
import os

text_file_path = 'Pushkin.txt'
checkpoint_path = "training_1/cp.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)
total_words = 0
max_sequence_len = 0
tokenizer = Tokenizer()


def get_raw_data_from_file(path):
    text = str()
    with open(path, "r", encoding="utf-8") as fd:
        text += fd.read()
    return text


def prepare_data(text_path):
    raw_text = get_raw_data_from_file(text_path)

    global tokenizer
    global max_sequence_len
    global total_words

    # Превращаем текст в токены (создаем word index)
    corpus = raw_text.split("\n\n")
    tokenizer.fit_on_texts(corpus)
    total_words = len(tokenizer.word_index) + 1

    # Разбиваем предложения на токены
    sequences = []
    for line in corpus:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i + 1]
            sequences.append(n_gram_sequence)

    # Делаем padding по наибольшему размеру
    sequence_lengths = list()
    for i in sequences:
        sequence_lengths.append(len(i))
    max_sequence_len = max(sequence_lengths)

    sequences = np.array(pad_sequences(sequences,
                                       maxlen=max_sequence_len + 1, padding='pre'))

    return sequences


def make_model(dropout_rate, activation_func, total, max_len):
    schema = [
        Embedding(total, 10, input_length=max_len),
        LSTM(32),
        Dropout(dropout_rate),
        Dense(32, activation=activation_func),
        Dropout(dropout_rate),
        Dense(total, activation=tf.nn.softmax)
    ]
    model = keras.Sequential(schema)
    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.categorical_crossentropy,
        metrics=['accuracy']
    )
    model.summary()

    return model


def predict(my_model, seed_text, seed=8):
    global tokenizer
    for _ in range(seed):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding='pre')
        predicted = np.argmax(my_model.predict(token_list), axis=1)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    print(seed_text)
    print("\n _____ \n")
    return seed_text


# def remove_repeats(s):
#     line = s.split()
#     k = []
#     for i in line:
#         if s.count(i) > 1 and (i not in k) or s.count(i) == 1:
#             k.append(i)
#     return ' '.join(k)


def letsgo(training, seed_text):
    input_sequences = prepare_data(text_file_path)
    x, y = input_sequences[:, :-1], input_sequences[:, -1]
    y = keras.utils.to_categorical(y, num_classes=total_words)
    my_model = make_model(0.3, keras.activations.relu, total_words, max_sequence_len)
    my_model.load_weights(checkpoint_path)
    if training:
        # Чтобы сохранить веса во время обучения
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                         save_weights_only=True,
                                                         verbose=1)
        my_model.fit(
            x,
            y,
            batch_size=50,
            epochs=15,
            callbacks=cp_callback
        )
    return predict(my_model, seed_text)


letsgo(True, "Зима")
