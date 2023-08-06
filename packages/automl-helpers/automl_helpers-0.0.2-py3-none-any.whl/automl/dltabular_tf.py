from typing import Any, Dict

import numpy as np
import pandas as pd
import math

import scipy.special
import sklearn.datasets
import sklearn.metrics
import sklearn.model_selection
import sklearn.preprocessing
from sklearn.preprocessing import OneHotEncoder

import tensorflow as tf

import matplotlib.pyplot as plt

from tensorflow.keras.optimizers import Adam
# from official.nlp import optimization

import tensorflow_addons as tfa

from tensorflow.keras import layers
from tensorflow.keras import initializers
from tensorflow.keras.layers import Dense, Activation, BatchNormalization, Dropout, ReLU, Add, PReLU, MultiHeadAttention



class MLP(tf.keras.Model):
    def __init__(self,  d_main: int, d_hidden: int, **kwargs ) -> None:
        super(MLP, self).__init__(**kwargs )
        
        self.dense1 = Dense(d_main)#d_main, d_hidden, bias_first)
        self.dense2 = Dense(d_hidden)

        # self.normalization = BatchNormalization()
        self.activation = PReLU()
        self.output_layer = Dense(1)     
        
    def call(self, inputs):
        x = self.dense1(inputs)
        x = self.activation(x)
        x = self.dense2(inputs)
        x = self.activation(x)
        x = self.output_layer(x)
        return x

class ResNetBlock(tf.keras.layers.Layer):
    """The main building block of `ResNet`."""

    def __init__( self, d_main: int, d_hidden: int, **kwargs ) -> None:  
        super(ResNetBlock, self).__init__( **kwargs)
        
        self.normalization = BatchNormalization()
        self.linear_first = Dense(d_hidden)#d_main, d_hidden, bias_first)
        self.activation = ReLU()
        self.dropout_first = Dropout(.2)
        self.linear_second = Dense(d_main)
        self.dropout_second = Dropout(0)
        self.skip_connection = True

    def call(self, x):
        x_input = x
        x = self.normalization(x)
        x = self.linear_first(x)
        x = self.activation(x)
        x = self.dropout_first(x)
        x = self.linear_second(x)
        x = self.dropout_second(x)
        if self.skip_connection:
            x = x_input + x
        return x

class ResNet(tf.keras.Model):
    def __init__(self,  d_main: int, d_hidden: int, **kwargs ) -> None:
        super(ResNet, self).__init__(**kwargs )
        
        self.linear_first = Dense(d_main)#d_main, d_hidden, bias_first)
        self.resnetblock1 = ResNetBlock(d_main,d_hidden)
        self.resnetblock2 = ResNetBlock(d_main,d_hidden)
        self.normalization = BatchNormalization()
        self.activation = PReLU()
        self.output_layer = Dense(1)     
        # self.output_skip = Dense(1)
        # self.add_layer = Add()
        
    def call(self, inputs):
        x = self.linear_first(inputs)
        #x1 = self.output_skip(inputs)
        x = self.resnetblock1(x)
        x = self.resnetblock2(x)
        x = self.normalization(x)
        x = self.activation(x)
        x = self.output_layer(x)
        #x = self.add_layer([x,x1])
        return x



class ResNetDR(tf.keras.Model):
    def __init__(self,  d_main: int, d_hidden: int, **kwargs ) -> None:
        super(ResNetDR, self).__init__(**kwargs )
        
        self.dense1 = Dense(d_main)#d_main, d_hidden, bias_first)
        self.dense2 = Dense(d_hidden)

        # self.normalization = BatchNormalization()
        self.activation = PReLU()
        self.output_layer = Dense(1)     
        self.output_skip = Dense(1)
        self.add_layer = Add()
        
    def call(self, inputs):
        x = self.dense1(inputs)
        x1 = self.output_skip(inputs)
        # x = self.resnetblock1(x)
        # x = self.resnetblock2(x)
        # x = self.normalization(x)
        x = self.activation(x)
        x = self.dense2(inputs)
        x = self.activation(x)
        x = self.output_layer(x)
        x = self.add_layer([x,x1])
        return x



class NumericalFeatureTokenizer(layers.Layer):
    """Transforms continuous features to tokens (embeddings).

    See `FeatureTokenizer` for the illustration.

    For one feature, the transformation consists of two steps:

    * the feature is multiplied by a trainable vector
    * another trainable vector is added

    Note that each feature has its separate pair of trainable vectors, i.e. the vectors
    are not shared between features.

    Examples:
        .. testcode::

            x = torch.randn(4, 2)
            n_objects, n_features = x.shape
            d_token = 3
            tokenizer = NumericalFeatureTokenizer(n_features, d_token, True, 'uniform')
            tokens = tokenizer(x)
            assert tokens.shape == (n_objects, n_features, d_token)
    """

    def __init__(
        self,
        n_features: int,
        d_token: int,
        bias: bool,
    ) -> None:
        """
        Args:
            n_features: the number of continuous (scalar) features
            d_token: the size of one token
            bias: if `False`, then the transformation will include only multiplication.
                **Warning**: :code:`bias=False` leads to significantly worse results for
                Transformer-like (token-based) architectures.
            initialization: initialization policy for parameters. Must be one of
                :code:`['uniform', 'normal']`. Let :code:`s = d ** -0.5`. Then, the
                corresponding distributions are :code:`Uniform(-s, s)` and :code:`Normal(0, s)`.
                In [gorishniy2021revisiting], the 'uniform' initialization was used.

        References:
            * [gorishniy2021revisiting] Yury Gorishniy, Ivan Rubachev, Valentin Khrulkov, Artem Babenko, "Revisiting Deep Learning Models for Tabular Data", 2021
        """
        super(NumericalFeatureTokenizer, self).__init__()
        
        self.W = self.add_weight("W",shape=(n_features, d_token), initializer= initializers.RandomUniform(minval=-1*d_token**(-.5), maxval=d_token**(-.5), seed=None))
        self.bias = self.add_weight("bias",shape=(n_features, d_token), initializer= initializers.RandomUniform(minval=-1*d_token**(-.5), maxval=d_token**(-.5), seed=None)) if bias else None

    @property
    def n_tokens(self) -> int:
        """The number of tokens."""
        return len(self.W)

    @property
    def d_token(self) -> int:
        """The size of one token."""
        return self.W.shape[1]

    def call(self, x):
        x = self.W[None] * x[..., None]
        if self.bias is not None:
            x = x + self.bias[None]
        return x



class TransformerBlock(layers.Layer):
    def __init__(self, embed_dim, num_heads, ff_dim, dropout_rate=0.1):
        super(TransformerBlock, self).__init__()
        self.att = MultiHeadAttention(num_heads=num_heads, key_dim=embed_dim, dropout=dropout_rate)
        self.ffn1 = Dense(ff_dim, activation="relu")
        self.ffn2=Dense(embed_dim)
        self.layernorm1 = layers.LayerNormalization(epsilon=1e-6)
        self.layernorm2 = layers.LayerNormalization(epsilon=1e-6)
        self.dropout1 = layers.Dropout(dropout_rate)
        self.dropout2 = layers.Dropout(dropout_rate)

    def call(self, inputs, training):
        attn_output = self.att(inputs, inputs)
        attn_output = self.dropout1(attn_output, training=training)
        out1 = self.layernorm1(inputs + attn_output)
        ffn_output = self.ffn1(out1)
        ffn_output = self.ffn2(ffn_output)
        ffn_output = self.dropout2(ffn_output, training=training)
        return self.layernorm2(out1 + ffn_output)


class CLSToken(layers.Layer):
    def __init__(self, embed_dim):
        super(CLSToken, self).__init__()
        self.W = self.add_weight("W",shape=(embed_dim,), initializer= initializers.RandomUniform(minval=-0.05, maxval=0.05, seed=None))#initializers.GlorotNormal(seed=None)
        
    def expand(self,leading_dimensions):
        if len(leading_dimensions)==0:
            return self.W
        new_d=(1,)*(len(leading_dimensions)-2)
        result=tf.reshape(self.W,shape=[*new_d,-1])    
        return tf.broadcast_to(result, [leading_dimensions[0],*new_d,result.shape[-1]])
        
    def call(self, inputs):
        result=self.expand(tf.shape(inputs))
        return tf.concat( [inputs,result], axis=1, name='concat')


class FTTransformer(tf.keras.Model):
    def __init__(self,n_num_features, n_cat_features, d_token, dropout_rate, ff_dim: int, d_out=1, **kwargs ) -> None:
        super(FTTransformer, self).__init__(**kwargs )

        num_heads=3
        ff_dim=32
        
        self.num_featurizer = NumericalFeatureTokenizer(n_num_features, d_token, True)
        self.cls_token = CLSToken(d_token)
        self.transformer1 = TransformerBlock(d_token, num_heads, ff_dim, dropout_rate)
        self.transformer2 = TransformerBlock(d_token, num_heads, ff_dim, dropout_rate)
        self.headnorm = layers.LayerNormalization(epsilon=1e-6)
        self.activation = ReLU()
        self.linear = Dense(d_out)
        
        
    def call(self, inputs):
        x = self.num_featurizer(inputs)
        x = self.cls_token(x)
        x = self.transformer1(x)
        x = self.transformer2(x)
        x = x[:, -1]
        x = self.headnorm(x)
        x = self.activation(x)
        x = self.linear(x)
        return x



class FTTransformerRes(tf.keras.Model):
    def __init__(self,n_num_features, n_cat_features, d_token, dropout_rate, ff_dim: int, d_out=1, **kwargs ) -> None:
        super(FTTransformerRes, self).__init__(**kwargs )

        num_heads=3
        ff_dim=32
        
        self.num_featurizer = NumericalFeatureTokenizer(n_num_features, d_token, True)
        self.cls_token = CLSToken(d_token)
        self.transformer1 = TransformerBlock(d_token, num_heads, ff_dim, dropout_rate)
        self.transformer2 = TransformerBlock(d_token, num_heads, ff_dim, dropout_rate)
        self.headnorm = layers.LayerNormalization(epsilon=1e-6)
        self.activation = ReLU()
        self.linear = Dense(d_out)
        self.output_skip = Dense(1)
        self.add_layer = Add()
        
        
    def call(self, inputs):
        x = self.num_featurizer(inputs)
        x1 = self.output_skip(inputs)
        x = self.cls_token(x)
        x = self.transformer1(x)
        x = self.transformer2(x)
        x = x[:, -1]
        x = self.headnorm(x)
        x = self.activation(x)
        x = self.linear(x)
        x = self.add_layer([x,x1])
        return x