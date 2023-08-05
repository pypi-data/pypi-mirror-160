from tensorflow.keras.layers import Conv1D, Dropout, Input, Add, Flatten, Dense, Conv1DTranspose
from tensorflow.keras.models import Model
from prot2vec.layers.transformer_block import TransformerBlock
from keras_pos_embd import PositionEmbedding


def add_resnet_block(x, kernel_count, kernel_size, activation, dropout):
    x = Conv1D(kernel_count, kernel_size, activation=activation, padding='same')(x)
    x = Dropout(dropout)(x)
    skip = x
    x = Conv1D(kernel_count, kernel_size, activation=activation, padding='same')(x)
    x = Dropout(dropout)(x)
    x = Add()([x, skip])

    return x


def get_model(seq_len=48, seq_depth=20, kernel_count=128, emb_size=256, n_layers=4, n_heads=8, ff_dim=1024,
              activation='relu',
              dropout=0.1):
    input_layer = Input(shape=(seq_len, seq_depth), name='input_layer')
    x = input_layer

    x = add_resnet_block(x, kernel_count, 5, activation, dropout)
    x = Conv1D(emb_size, 5, activation=activation, padding='same', strides=3)(x)
    x = Dropout(dropout)(x)

    x = PositionEmbedding(input_dim=seq_len, output_dim=emb_size, mode=PositionEmbedding.MODE_ADD)(x)

    for i in range(n_layers):
        x = TransformerBlock(embed_dim=emb_size, num_heads=n_heads, ff_dim=ff_dim)(x)

    x = Conv1DTranspose(emb_size, 5, padding='same', strides=3)(x)
    x = Dropout(dropout)(x)

    x = add_resnet_block(x, kernel_count, 5, activation, dropout)

    x = Dense(seq_depth, activation='softmax')(x)

    output_layer = x

    model = Model(
        inputs=input_layer,
        outputs=output_layer,
        name='cnn_bert')

    return model


if __name__ == '__main__':
    model = get_model()
    print()
