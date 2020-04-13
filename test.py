import json
import numpy as np
from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_accuracy, crf_viterbi_accuracy
from keras.models import Model, Input
from keras.layers import Dense, Bidirectional, Dropout, LSTM, TimeDistributed, Masking
from keras.utils import to_categorical, plot_model
from seqeval.metrics import classification_report
import matplotlib.pyplot as plt

from utils import event_type
from utils import MAX_SEQ_LEN, train_file_path, test_file_path, dev_file_path
from load_data import read_data
from albert_zh.extract_feature import BertVector



# Bert Embeddings
bert_output = Input(shape=(128, 312,), name="bert_output")
# LSTM model
lstm = Bidirectional(LSTM(units=128, return_sequences=True), name="bi_lstm")(bert_output)
drop = Dropout(0.1, name="dropout")(lstm)
dense = TimeDistributed(Dense(8, activation="softmax"), name="time_distributed")(drop)
crf = CRF(8)
out = crf(dense)
model = Model(inputs=bert_output, outputs=out)
# model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.compile(loss=crf.loss_function, optimizer='adam', metrics=[crf.accuracy])

# 模型结构总结
model.summary()
plot_model(model, to_file="test.png", show_shapes=True)

