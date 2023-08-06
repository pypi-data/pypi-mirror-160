from tensorflow.keras.layers import Conv1D, Dropout, Input, Add, Flatten, Dense
from tensorflow.keras.models import Model
from keras_pos_embd import PositionEmbedding
from prot2vec.layers.transformer_block import TransformerBlock


def add_resnet_block(x, kernel_count, kernel_size, activation, dropout):
    x = Conv1D(kernel_count, kernel_size, activation=activation, padding='same')(x)
    x = Dropout(dropout)(x)
    skip = x
    x = Conv1D(kernel_count, kernel_size, activation=activation, padding='same')(x)
    x = Dropout(dropout)(x)
    x = Add()([x, skip])

    return x


def get_cnn_decipher_model(ciphers_n=100, seq_len=24, seq_depth=21, dropout=0.1, base_k_count=256):
    input_layer = Input(shape=(seq_len, seq_depth), name='input_layer')

    # (None, 24, seq_depth)
    x = input_layer

    # (None, 24, 256)
    x = add_resnet_block(x, base_k_count, 5, 'relu', dropout)

    # reduce -> 12
    x = Conv1D(base_k_count, 5, activation='relu', padding='same', strides=2)(x)
    x = Dropout(dropout)(x)

    # (None, 12, 512)
    x = add_resnet_block(x, base_k_count * 2, 5, 'relu', dropout)

    # reduce -> 6
    x = Conv1D(base_k_count * 2, 3, activation='relu', padding='same', strides=3)(x)
    x = Dropout(dropout)(x)

    # (None, 4, 1024)
    x = add_resnet_block(x, base_k_count * 4, 3, 'relu', dropout)

    # (None, 4096)
    x = Flatten()(x)

    # (None, 32)
    x = Dense(32, activation=None)(x)
    x = Dropout(dropout)(x)

    # (None, 100)
    output_layer = Dense(ciphers_n, activation='softmax')(x)

    model = Model(
        inputs=input_layer,
        outputs=output_layer,
        name='conv1D_decipher')

    return model


def get_cnn_transformer_decipher_model(ciphers_n=100, seq_len=24, seq_depth=21, dropout=0.1, kernel_count=128,
                                       emb_size=256, n_layers=4, n_heads=8, ff_dim=1024, activation='relu'):
    input_layer = Input(shape=(seq_len, seq_depth), name='input_layer')
    x = input_layer

    x = add_resnet_block(x, kernel_count, 5, activation, dropout)
    x = Conv1D(emb_size, 5, activation=activation, padding='same', strides=3)(x)
    x = Dropout(dropout)(x)

    x = PositionEmbedding(input_dim=seq_len, output_dim=emb_size, mode=PositionEmbedding.MODE_ADD)(x)

    for i in range(n_layers):
        x = TransformerBlock(embed_dim=emb_size, num_heads=n_heads, ff_dim=ff_dim)(x)

    x = Flatten()(x)
    x = Dense(ciphers_n, activation=None)(x)
    output_layer = Dense(ciphers_n, activation='softmax')(x)

    model = Model(
        inputs=input_layer,
        outputs=output_layer,
        name='cnn_bert_decipher')

    return model


if __name__ == '__main__':
    # model = get_cnn_decipher_model()
    model = get_cnn_transformer_decipher_model()
    print()
