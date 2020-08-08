"""
model_definition.py - This file contains the ModelDefinition class which encapsulates logic related to defining
the model layers.
"""
import os
from bert.loader import StockBertConfig, map_stock_config_to_params, load_stock_weights
import tensorflow as tf
from tensorflow import keras
from bert import BertModelLayer
from bert.tokenization.bert_tokenization import FullTokenizer
from build_configuration import BuildConfiguration


class ModelDefinition:
    """
    ModelDefinition - Class - The ModelDefinition class encapsulates logic related to defining the model
    architecture.
    """
    BERT_DIR = os.getenv("BERT_DIR", os.path.join(BuildConfiguration.BASE_DIR, "bert"))
    os.makedirs(BERT_DIR, exist_ok=True)

    BERT_CONFIG = os.getenv("BERT_CONFIG", os.path.join(BERT_DIR, "bert_config.json"))

    BERT_MODEL = os.getenv("BERT_MODEL", os.path.join(BERT_DIR, "bert_model.ckpt"))

    tokenizer = FullTokenizer(
        vocab_file=os.path.join(BERT_DIR, "vocab.txt")
    )

    @staticmethod
    def create_model(max_sequence_length, number_of_intents):
        """
        ModelDefinition.create_model - Method - The create_model method is a helper which accepts
        max input sequence length and the number of intents (or bins/buckets). The logic returns a
        BERT model that matches the specified architecture.

        :param max_sequence_length: maximum length of input sequence
        :type max_sequence_length: int
        :param number_of_intents: number of classifiable bins/buckets
        :type number_of_intents: int
        :return: model definition
        :rtype: keras.Model
        """

        with tf.io.gfile.GFile(ModelDefinition.BERT_CONFIG) as reader:
            bc = StockBertConfig.from_json_string(reader.read())
            bert_params = map_stock_config_to_params(bc)
            bert_params.adapter_size = None
            bert = BertModelLayer.from_params(bert_params, name="bert")

        input_ids = keras.layers.Input(shape=(max_sequence_length,), dtype='int32', name="input_ids")
        bert_output = bert(input_ids)

        cls_out = keras.layers.Lambda(lambda seq: seq[:, 0, :])(bert_output)
        cls_out = keras.layers.Dropout(0.5)(cls_out)
        logits = keras.layers.Dense(units=768, activation="tanh")(cls_out)
        logits = keras.layers.Dropout(0.5)(logits)
        logits = keras.layers.Dense(units=number_of_intents, activation="softmax")(logits)

        model = keras.Model(inputs=input_ids, outputs=logits)
        model.build(input_shape=(None, max_sequence_length))

        load_stock_weights(bert, ModelDefinition.BERT_MODEL)

        return model
