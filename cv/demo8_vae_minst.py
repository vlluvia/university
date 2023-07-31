import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras import Sequential, layers, optimizers, Model
from PIL import Image
import os

tf.random.set_seed(22)
np.random.seed(22)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
assert tf.__version__.startswith('2.')

h_dim = 20
batchsz = 512
lr = 1e-3

(train_x, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
train_x, x_test = train_x.astype(np.float32) / 255., x_test.astype(np.float32) / 255.
nsample = 20
train_db = tf.data.Dataset.from_tensor_slices(train_x)
train_db = train_db.shuffle(batchsz * 5).batch(batchsz)

z_dim = 10

class VAE(tf.keras.Model):

    def __init__(self):
        super(VAE, self).__init__()

        # Encoder
        self.fc1 = layers.Dense(128)
        self.fc2 = layers.Dense(z_dim) # get mean prediction
        self.fc3 = layers.Dense(z_dim)

        # Decoder
        self.fc4 = layers.Dense(128)
        self.fc5 = layers.Dense(784)

    def encoder(self, x):

        h = tf.nn.relu(self.fc1(x))
        # get mean
        mu = self.fc2(h)
        # get variance
        log_var = self.fc3(h)

        return mu, log_var

    def decoder(self, z):

        out = tf.nn.relu(self.fc4(z))
        out = self.fc5(out)

        return out

    def reparameterize(self, mu, log_var):

        eps = tf.random.normal(log_var.shape)

        std = tf.exp(log_var*0.5)

        z = mu + std * eps
        return z

    def call(self, inputs, training=None):

        # [b, 784] => [b, z_dim], [b, z_dim]
        mu, log_var = self.encoder(inputs)
        # reparameterization trick
        z = self.reparameterize(mu, log_var)

        x_hat = self.decoder(z)

        return x_hat, mu, log_var

model = VAE()
model.build(input_shape=(4, 784))
optimizer = optimizers.Adam(lr)


for epoch in range(10):
    for step, x in enumerate(train_db):
        x = tf.reshape(x, [-1, 784])
        with tf.GradientTape() as tape:
            x_rec_logits, mu, log_var = model(x)

            rec_loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=x, logits=x_rec_logits)
            rec_loss = tf.reduce_sum(rec_loss) / x.shape[0]
            kl_div = -0.5 * (log_var + 1 - mu ** 2 - tf.exp(log_var))
            kl_div = tf.reduce_sum(kl_div) / x.shape[0]

            loss = rec_loss + 1. * kl_div

        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        if step % 100 == 0:
            print(epoch, step, 'kl div:', float(kl_div), 'rec loss:', float(rec_loss))

    print("Epoch{}/{}".format(epoch + 1, 10))

    z = tf.random.normal((20, z_dim))
    logits = model.decoder(z)
    x_hat = tf.sigmoid(logits)
    x_hat = tf.reshape(x_hat, [-1, 28, 28, 1]).numpy() * 255.
    x_hat = x_hat.astype(np.uint8)
    print(x_hat.shape)
    fig = plt.figure(figsize=(20, 1))

    for i in range(20):
        plt.subplot(1, 20, i + 1)
        plt.imshow(x_hat[i, :, :, 0] , cmap='binary')
        plt.axis('off')

    plt.show()
